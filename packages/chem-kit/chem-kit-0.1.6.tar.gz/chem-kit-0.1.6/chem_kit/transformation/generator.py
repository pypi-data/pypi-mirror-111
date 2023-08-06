from typing import Any, List, Iterable
from rdkit import Chem
from rdkit.Chem import rdFMCS
from chem_kit.molecule import Molecule, AROMATICITY_MODEL


class SmartsGenerator:

    EXPLICIT_H_MAP_FROM = 1000

    def __init__(self, *arg: Any, **kwargs: Any):
        self.smarts: str = self.get_smarts(*arg)

    def get_smarts(self, *source: Any) -> str:
        mols = self.list_mols(*source)
        mols = [Chem.AddHs(mol) for mol in mols]
        matches = self.get_common_atoms(*mols)
        self.map_matches(matches, mols)
        h_mapped = self.get_h_mapped(mols)
        mols = [self.remove_h_non_mapped(mol) for mol in mols]
        mols = self.explicit_h_when_mapped_with_h(mols, h_mapped)
        mols_smarts = [Chem.MolToSmarts(mol) for mol in mols]
        return ">>".join(mols_smarts)

    @staticmethod
    def get_h_mapped(mols: Iterable[Chem.Mol]) -> List[int]:
        h_mapped = []
        for mol in mols:
            for atom in mol.GetAtoms():
                map_num = atom.GetAtomMapNum()
                if atom.GetAtomicNum() == 1 and map_num != 0:
                    h_mapped.append(map_num)
        return h_mapped

    @staticmethod
    def explicit_h_when_mapped_with_h(
        mols: Iterable[Chem.Mol], h_mapped: List[int]
    ) -> List[Chem.Mol]:
        mols_res = []
        for mol in mols:
            mol = Chem.MolFromSmarts(Chem.MolToSmarts(mol))
            mol.UpdatePropertyCache(strict=False)
            idxs = [
                atom.GetIdx()
                for atom in mol.GetAtoms()
                if (atom.GetAtomMapNum() in h_mapped)
            ]
            if idxs:
                mol = Chem.AddHs(mol, onlyOnAtoms=idxs)
            mols_res.append(mol)
        return mols_res

    def list_mols(self, *smarts: str) -> Iterable[Chem.Mol]:
        mols = [Chem.MolFromSmarts(sm) for sm in smarts]
        for mol in mols:
            Chem.SanitizeMol(mol)
        return mols

    def get_common_atoms(self, *mols: Chem.Mol) -> List[Chem.Mol]:
        mcs = rdFMCS.FindMCS(
            mols,
            atomCompare=rdFMCS.AtomCompare.CompareAny,
            # atomCompare=rdFMCS.AtomCompare.CompareElements,
            bondCompare=rdFMCS.BondCompare.CompareAny,
            # ringCompare=Chem.rdFMCS.RingCompare.StrictRingFusion,
            # ringCompare=Chem.rdFMCS.RingCompare.PermissiveRingFusion,
            # ringMatchesRingOnly=True,
            # completeRingsOnly=True,
        ).queryMol
        return [mol.GetSubstructMatch(mcs) for mol in mols]

    @staticmethod
    def map_matches(matches: Iterable[Chem.Mol], mols: Iterable[Chem.Mol]) -> None:
        map_count = 1
        for atoms_idx in zip(*matches):
            atoms = [mol.GetAtomWithIdx(idx) for mol, idx in zip(mols, atoms_idx)]
            if set(atom.GetSymbol() for atom in atoms) != {"H"}:
                [atom.SetAtomMapNum(map_count) for atom in atoms]
                map_count += 1

    def remove_h_non_mapped(self, mol: Chem.Mol) -> Chem.RWMol:
        rwmol = Chem.RWMol(mol)
        atoms_to_remove = []
        for atom in rwmol.GetAtoms():
            if atom.GetAtomMapNum() == 0 and atom.GetSymbol() == "H":
                atoms_to_remove.append(atom.GetIdx())
            if atom.GetAtomMapNum() > self.EXPLICIT_H_MAP_FROM:
                atom.SetAtomMapNum(0)
        atoms_to_remove.sort(reverse=True)
        for idx in atoms_to_remove:
            rwmol.RemoveAtom(idx)
        return rwmol


class SmartsFromSmiles(SmartsGenerator):
    def list_mols(self, *smiles: str) -> List[Chem.Mol]:
        mols = [Molecule(sm, preserve_H=True).rdkit for sm in smiles]
        for mol in mols:
            h_map_idx = self.EXPLICIT_H_MAP_FROM + 1
            for atom in mol.GetAtoms():
                if atom.GetAtomicNum() == 1:
                    atom.SetAtomMapNum(h_map_idx)
                    h_map_idx += 1
        return mols


class SmartsFromMetWorkV0(SmartsGenerator):
    def get_smarts(self, *smarts_: str) -> str:
        smarts = smarts_[0]
        smarts = smarts.replace("=,:", "=")
        smarts_list = smarts.split(">>")
        mols = [Chem.MolFromSmarts(sm) for sm in smarts_list]
        mols = [self.unset_mapping(mol) for mol in mols]
        for mol in mols:
            Chem.Kekulize(mol)
            Chem.SetAromaticity(mol, AROMATICITY_MODEL)
        return super().get_smarts(*mols)

    @staticmethod
    def list_mols(*source: str) -> Iterable[str]:
        return source

    @staticmethod
    def unset_mapping(mol: Chem.Mol) -> Chem.Mol:
        for atom in mol.GetAtoms():
            atom.SetAtomMapNum(0)
        return mol
