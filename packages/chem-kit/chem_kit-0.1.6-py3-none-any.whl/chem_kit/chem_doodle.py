import re
from typing import Dict, List, Union, Optional, Any
from pydantic import BaseModel, Field
from rdkit import Chem


class AtomQasJsonModel(BaseModel):
    v: List[str]
    n: bool


class AtomQJsonModel(BaseModel):
    as_: AtomQasJsonModel = Field(None, alias="as")


class AtomJsonModel(BaseModel):
    i: str = Field(..., description="Atom index")
    x: float = Field(..., description="X position")
    y: float = Field(..., description="Y position")
    l_: str = Field(None, alias="l", description="label")
    q: Optional[AtomQJsonModel]
    c: Optional[int]


class BondJsonModel(BaseModel):
    i: str = Field(..., description="Bond index")
    b: int = Field(..., description="Atom begin")
    e: int = Field(..., description="Atom end")
    o: Optional[int]
    s: Optional[str]


class MolJsonModel(BaseModel):
    a: List[AtomJsonModel] = Field([], description="Atoms list")
    b: List[BondJsonModel] = Field([], description="Bonds list")


class ReactJsonModel(BaseModel):
    m: List[MolJsonModel] = Field([], description="Molecules list")
    s: List[Dict[str, Union[Optional[str], float]]] = Field(
        [], description="Shapes list"
    )


class ChemDoodle:
    data: BaseModel

    def to_dict(self) -> Dict[str, Any]:
        return self.data.dict(by_alias=True, exclude_none=True)


class ChemDoodleReaction(ChemDoodle):
    """
    Utils to use [ChemDoolde JSON format]\
(https://web.chemdoodle.com/docs/chemdoodle-json-format)
    """

    PADDING = 80
    ARROW_LENGTH = 60
    data: ReactJsonModel

    def __init__(self, reaction: Chem.rdChemReactions.ChemicalReaction):
        self.begin_id = {"a": 0, "b": 0}
        self.x_bound = 0.0
        self.atom_maping: Dict[str, Any] = {}
        self.data = ReactJsonModel()
        self.reaction = reaction
        self.set_reactants()
        self.set_arrows()
        self.set_products()
        self.set_atom_mapping()

    def set_reactants(self) -> None:
        for m in self.reaction.GetReactants():
            self.x_bound += self.append_mol(m, "reactant") + self.PADDING

    def set_arrows(self) -> None:
        self.x_bound -= self.PADDING / 2
        self.data.s.append(
            {
                "i": "s0",
                "t": "Line",
                "x1": self.x_bound,
                "y1": 0.0,
                "x2": self.x_bound + self.ARROW_LENGTH,
                "y2": 0.0,
                "a": "synthetic",
            }
        )
        self.x_bound += self.ARROW_LENGTH + self.PADDING

    def set_products(self) -> None:
        for m in self.reaction.GetProducts():
            self.x_bound += self.append_mol(m, "product")

    def set_atom_mapping(self) -> None:
        for i, map_ in self.atom_maping.items():
            self.data.s.append(
                {
                    "i": "s{0}".format(i),
                    "t": "AtomMapping",
                    "a1": map_[0],
                    "a2": map_[1],
                }
            )

    def append_mol(self, mol_rdkit: Chem.Mol, mol_type: str) -> float:
        cd_mol = ChemDoodleMolecule(mol_rdkit, self.begin_id)
        mol_data = cd_mol.data
        # self.begin_id = cd_mol.begin_id
        x_max = 0.0
        x_min = 0.0
        for a in mol_data.a:
            x_min = min(x_min, a.x)
        for a in mol_data.a:
            a.x += self.x_bound - x_min
            x_max = max(x_max, a.x)
        for i, atom in enumerate(mol_rdkit.GetAtoms()):
            map_num = atom.GetAtomMapNum()
            if map_num > 0:
                atom_id = "a{0}".format(i + self.begin_id["a"])
                if mol_type == "reactant":
                    self.atom_maping[map_num] = [atom_id, None]
                elif mol_type == "product":
                    self.atom_maping[map_num][1] = atom_id
        self.data.m.append(mol_data)
        self.begin_id["a"] += len(mol_data.a)
        self.begin_id["b"] += len(mol_data.b)

        return x_max


class ChemDoodleMolecule(ChemDoodle):
    data: MolJsonModel
    ZOOM = 20
    BOND_TYPE_DIC = {
        Chem.rdchem.BondType.SINGLE: 1,
        Chem.rdchem.BondType.DOUBLE: 2,
        Chem.rdchem.BondType.TRIPLE: 3,
    }
    CHIRAL_CONFIG = {
        Chem.rdchem.ChiralType.CHI_TETRAHEDRAL_CCW: {
            0: "protruding",
            2: "recessed",
        },
        Chem.rdchem.ChiralType.CHI_TETRAHEDRAL_CW: {0: "recessed", 2: "protruding"},
    }

    def __init__(self, molecule: Chem.Mol, begin_id: Dict[str, int]) -> None:

        self.chiral_bonds: Dict[int, Any] = {}
        self.data = MolJsonModel()
        self.begin_id = begin_id
        self.molecule = molecule
        self.molecule.UpdatePropertyCache()
        Chem.rdDepictor.Compute2DCoords(self.molecule)

        self.set_atoms()
        self.set_aromaticity()
        self.set_bonds()

    def set_atoms(self) -> None:
        positions = self.molecule.GetConformer().GetPositions()
        for i, a in enumerate(self.molecule.GetAtoms()):
            atom_json = AtomJsonModel(
                i="a{0}".format(i + self.begin_id["a"]),
                x=self.ZOOM * positions[i][0],
                y=self.ZOOM * positions[i][1],
            )
            symbols = re.findall(r"\[([^:]*?)(?:\:\d)?\]", a.GetSmarts())
            if len(symbols) > 0:
                symbols = symbols[0].split(",")
            if "*" in symbols:
                self.set_atom_q(atom_json, ["a"])
            elif len(symbols) > 1:
                values = []
                for sy in symbols:
                    match = re.search(r"#(\d)", sy)
                    if match:
                        at_value = int(match.group(1))
                        values.append(Chem.Atom(at_value).GetSymbol())
                    else:
                        values.append(sy)
                self.set_atom_q(atom_json, values)
            else:
                symbol: str = a.GetSymbol()
                if symbol != "C":
                    atom_json.l_ = symbol
                charge: int = a.GetFormalCharge()
                if charge != 0:
                    atom_json.c = charge
                elif a.GetChiralTag() != Chem.rdchem.ChiralType.CHI_UNSPECIFIED:
                    ct = a.GetChiralTag()
                    for i, b in enumerate(a.GetBonds()):
                        if i in self.CHIRAL_CONFIG[ct]:
                            self.chiral_bonds[b.GetIdx()] = self.CHIRAL_CONFIG[ct][i]
            self.data.a.append(atom_json)

    def set_atom_q(self, atom_json: AtomJsonModel, values: List[str]) -> None:
        kwargs = {"as": AtomQasJsonModel(v=values, n=False)}
        atom_json.q = AtomQJsonModel(**kwargs)

    def set_aromaticity(self) -> None:

        Chem.rdmolops.SanitizeMol(self.molecule)
        Chem.Kekulize(self.molecule, True)

        # try:
        #     # Force atom to be aromatic if is in ring
        #     #  FIXME: Why force aromatics ???
        #     for atom in self.molecule.GetAtoms():
        #         atom.SetIsAromatic(atom.IsInRing())
        #     # Kekulize mol
        #     Chem.rdmolops.SanitizeMol(self.molecule)
        #     Chem.Kekulize(self.molecule, True)
        # except Exception:
        #     # Transform aromatic bonds in kekulize form
        #     # This should not be used ...
        #     arom_bond_type = Chem.rdchem.BondType.SINGLE

        #     def propagate_kekulize(
        #         atom: Chem.Atom, arom_bond_type: Chem.BondType
        #     ) -> None:
        #         for b in atom.GetBonds():
        #             if b.GetBondType() == Chem.rdchem.BondType.AROMATIC:
        #                 if arom_bond_type == Chem.rdchem.BondType.SINGLE:
        #                     arom_bond_type = Chem.rdchem.BondType.DOUBLE
        #                 else:
        #                     arom_bond_type = Chem.rdchem.BondType.SINGLE
        #                 b.SetBondType(arom_bond_type)
        #                 if atom.GetIdx() != b.GetBeginAtomIdx():
        #                     target = b.GetBeginAtom()
        #                 else:
        #                     target = b.GetEndAtom()
        #                 propagate_kekulize(target, arom_bond_type)

        #     for b in self.molecule.GetBonds():
        #         if b.GetBondType() == Chem.rdchem.BondType.AROMATIC:
        #             b.SetBondType(arom_bond_type)
        #             propagate_kekulize(b.GetBeginAtom(), arom_bond_type)

    def set_bonds(self) -> None:
        for i, b in enumerate(self.molecule.GetBonds()):
            b_id = b.GetIdx()
            bond_json = BondJsonModel(
                i="b{0}".format(i + self.begin_id["b"]),
                b=b.GetBeginAtomIdx(),
                e=b.GetEndAtomIdx(),
            )
            bond_type = b.GetBondType()
            if bond_type != Chem.rdchem.BondType.SINGLE:
                bond_json.o = self.BOND_TYPE_DIC[bond_type]
            if b_id in self.chiral_bonds:
                bond_json.s = self.chiral_bonds[b_id]
            self.data.b.append(bond_json)
