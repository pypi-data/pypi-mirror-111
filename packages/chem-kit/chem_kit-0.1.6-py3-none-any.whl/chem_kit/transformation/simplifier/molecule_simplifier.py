from __future__ import annotations
from typing import List, Set, Dict, Tuple, Any, Iterable
from rdkit import Chem
from chem_kit.molecule import Molecule
from .params import SimplifierParams


class MoleculeSimplifier:
    def __init__(self, mol: Chem.Mol, params: SimplifierParams):
        self.params = params
        mol = Molecule.resolve_charge(mol)
        self.mol = mol
        self.mol_smiles = Molecule(Chem.MolToSmiles(mol), preserve_H=True)
        self.map_to_keep: Set[int] = set()

    def append_map_to_keep(self, value: int) -> None:
        self.map_to_keep = self.map_to_keep | {value}

    def init_keep(self) -> None:
        matched_atoms = getattr(self.mol, "__sssAtoms")
        all_idx = {atom.GetIdx() for atom in self.mol.GetAtoms()}
        idx_to_keep = all_idx - set(matched_atoms)
        self.map_to_keep = {
            self.mol.GetAtomWithIdx(idx).GetAtomMapNum() for idx in idx_to_keep
        } | {0}

    def propagate_map_to_keep(self) -> None:
        self.propagate_hetero(to_connector=True)
        if self.params.cycles:
            self.propagate_ring()
            self.propagate_hetero(to_connector=False)

    def propagate_hetero(self, to_connector: bool) -> None:
        mol_smiles = self.mol_smiles.rdkit
        for idx in self.idx_to_keep_from_map(mol_smiles):
            atom = mol_smiles.GetAtomWithIdx(idx)
            visitor = AtomVisitor(self, atom, params=self.params)
            visitor.propagate(to_connector=to_connector)

    def propagate_ring(self) -> None:
        mol_smiles = self.mol_smiles
        systems = mol_smiles.get_ring_systems()
        idx_to_keep: Set[int] = set([])

        for atom in mol_smiles.get_atoms():
            if atom.GetAtomMapNum() in self.map_to_keep:
                for system in systems:
                    if atom.GetIdx() in system:
                        idx_to_keep = idx_to_keep | system

        map_to_keep = self.map_to_keep
        systems_to_keep = {
            mol_smiles.rdkit.GetAtomWithIdx(idx).GetAtomMapNum() for idx in idx_to_keep
        }
        map_to_keep = map_to_keep | systems_to_keep
        self.map_to_keep = map_to_keep

    def get_idx_to_remove(self) -> List[int]:
        mol = self.mol
        idx_to_keep = self.idx_to_keep_from_map(mol)
        all_idx = {atom.GetIdx() for atom in mol.GetAtoms()}
        idx_to_remove = list(all_idx - idx_to_keep)
        idx_to_remove.sort(reverse=True)
        return idx_to_remove

    def remove_atoms(self) -> None:
        idx_to_remove = self.get_idx_to_remove()
        rwmol = Chem.RWMol(self.mol)
        for idx in idx_to_remove:
            rwmol.RemoveAtom(idx)
        self.mol = rwmol

    def idx_to_keep_from_map(self, mol: Chem.Mol) -> Set[int]:
        return {
            atom.GetIdx()
            for atom in mol.GetAtoms()
            if atom.GetAtomMapNum() in self.map_to_keep
        }

    def get_bond_types(self) -> Dict[Tuple[int, int], int]:
        bond_types = dict()
        for bond in self.mol.GetBonds():
            mapped_atoms = [
                bond.GetBeginAtom().GetAtomMapNum(),
                bond.GetEndAtom().GetAtomMapNum(),
            ]
            mapped_atoms.sort()

            if all(mapped_atoms):
                bond_types[tuple(mapped_atoms)] = bond.GetBondType()
        return bond_types  # type: ignore


class AtomVisitor:
    def __init__(
        self,
        mol_simplifier: MoleculeSimplifier,
        atom: Chem.Atom,
        params: SimplifierParams,
    ):
        self.params = params
        self.mol_simplifier = mol_simplifier
        self.atom = atom

    @property
    def is_hetero(self) -> bool:
        return self.atom.GetAtomicNum() != 6  # type: ignore

    @property
    def is_aromatic(self) -> bool:
        return self.atom.GetIsAromatic()  # type: ignore

    @property
    def map_num(self) -> int:
        return self.atom.GetAtomMapNum()  # type: ignore

    @property
    def is_keeped(self) -> bool:
        return self.map_num in self.mol_simplifier.map_to_keep

    def to_propagate_from(
        self, from_visitor: AtomVisitor, bond: Chem.Bond, to_connector: bool
    ) -> Tuple[bool, bool]:
        if from_visitor.is_keeped and self.is_keeped:
            return False, False
        if from_visitor.is_aromatic and self.is_aromatic and self.params.aromatic:
            return True, False
        if bond.GetIsConjugated() and self.params.conjugated:
            return True, to_connector
        if self.is_hetero and self.params.hetero_atoms:
            return True, to_connector
        if from_visitor.is_hetero and self.params.hetero_atoms and to_connector:
            return True, self.is_hetero
        return to_connector, False

    def set_keep(self) -> None:
        self.mol_simplifier.append_map_to_keep(self.map_num)

    def propagate(self, to_connector: bool) -> None:
        for atom, bond in self.connected_atoms():
            visitor = self.__class__(self.mol_simplifier, atom, params=self.params)
            propagate, to_connector = visitor.to_propagate_from(
                self, bond, to_connector=to_connector
            )
            if propagate:
                visitor.set_keep()
                visitor.propagate(to_connector=to_connector)

    def connected_atoms(self) -> Iterable[Any]:
        for bond in self.atom.GetBonds():
            for atom in (bond.GetBeginAtom(), bond.GetEndAtom()):
                if atom.GetIdx() != self.atom.GetIdx():
                    yield atom, bond
