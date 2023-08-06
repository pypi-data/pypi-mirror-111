import re
from typing import List, Set, Iterable, Any, Tuple
from rdkit import Chem
from rdkit.Chem import rdFMCS
from .params import SimplifierParams
from .molecule_simplifier import MoleculeSimplifier


class TransformationSimplifier:

    simplified_smarts: List[str] = []

    def __init__(self, smarts: str, **params: SimplifierParams):
        self.params = SimplifierParams(**params)
        self._full_smarts = smarts
        self.simplify_smarts()

    @property
    def full_smarts(self) -> str:
        return self._full_smarts

    def simplify_smarts(self) -> None:
        mols = [Chem.MolFromSmarts(sm) for sm in self.full_smarts.split(">>")]
        mcs = rdFMCS.FindMCS(mols).queryMol

        _ = [mol.GetSubstructMatch(mcs) for mol in mols]

        mol_simplifiers = [MoleculeSimplifier(mol, self.params) for mol in mols]

        for ms in mol_simplifiers:
            ms.init_keep()

        self.keep_for_bond_diff(mol_simplifiers)

        for ms in mol_simplifiers:
            ms.propagate_map_to_keep()

        self.keep_for_bond_diff(mol_simplifiers)

        self.join_mapped_atoms(mol_simplifiers)

        smarts = [Chem.MolToSmarts(ms.mol) for ms in mol_simplifiers]
        splits = [sm.split(".") for sm in smarts]

        splits = [
            [
                {
                    "smarts": sm,
                    "mapped": set(re.findall(r"\[#\d+(?:\&(?:\++|-))?:(\d+)\]", sm)),
                }
                for sm in split
            ]
            for split in splits
        ]
        smarts = []
        for dic1 in splits[0]:
            for dic2 in splits[1]:
                if dic1["mapped"] == dic2["mapped"]:
                    smarts.append(">>".join([dic1["smarts"], dic2["smarts"]]))

        smarts = list(set(smarts) - {">>"})

        self.simplified_smarts = smarts

    def join_mapped_atoms(self, mol_simplifiers: Iterable[MoleculeSimplifier]) -> None:
        map_to_keep: Set[int] = set([])
        for ms in mol_simplifiers:
            map_to_keep = map_to_keep | ms.map_to_keep
        for ms in mol_simplifiers:
            ms.map_to_keep = map_to_keep
            ms.remove_atoms()

    @staticmethod
    def keep_for_bond_diff(mol_simplifiers: Iterable[MoleculeSimplifier]) -> None:
        map_to_keep: Set[int] = set()
        bond_types = [ms.get_bond_types() for ms in mol_simplifiers]
        bond_types_keys_: Iterable[Set[Tuple[int, int]]] = [
            set(bond_type.keys()) for bond_type in bond_types
        ]
        bond_types_keys: Set[Tuple[int, int]] = set()
        bond_types_keys = bond_types_keys.union(*bond_types_keys_)
        for key in bond_types_keys:
            values: Set[Any] = set(
                [bond_type.get(key, tuple()) for bond_type in bond_types]
            )
            if len(values) > 1:
                map_to_keep = map_to_keep | set(key)
        for ms in mol_simplifiers:
            ms.map_to_keep = ms.map_to_keep | map_to_keep
