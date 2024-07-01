use anyhow::{Context, Result};
use std::{
    collections::{HashMap, HashSet},
    str::FromStr,
};

fn main() -> Result<()> {
    let input = include_str!("../data/input.txt").trim();
    println!("Problem 1: {}", problem1(input)?);
    println!("Problem 2: {}", problem2(input)?);
    Ok(())
}

struct Machine {
    replacements: HashMap<String, Vec<String>>,
}

impl FromStr for Machine {
    type Err = anyhow::Error;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let mut replacements = HashMap::new();
        for line in s.lines() {
            let (from, to) = line.split_once(" => ").context("Invalid line: no ' => '")?;
            replacements
                .entry(from.to_string())
                .or_insert(vec![])
                .push(to.to_string());
        }
        Ok(Self { replacements })
    }
}

impl Machine {
    fn step(&self, mut molecules: Vec<String>) -> HashSet<String> {
        let mut new_molecules: HashSet<String> = HashSet::new();
        let num_molecules = molecules.len();
        for i in 0..num_molecules {
            if let Some(molecule_replacements) = self.replacements.get(&molecules[i]) {
                let original = molecules[i].clone();
                for replacement in molecule_replacements {
                    molecules[i] = replacement.clone();
                    new_molecules.insert(molecules.join(""));
                }
                molecules[i] = original;
            }
        }
        new_molecules
    }

    fn make_medicine(&self, target_molecule: &str) -> Result<u32> {
        let mut molecules: HashSet<String> = self
            .replacements
            .get("e")
            .context("No e")?
            .clone()
            .into_iter()
            .collect();
        let mut already_transformed: HashSet<String> = HashSet::new();
        for step in 2..usize::MAX {
            if step % 5 == 0 {
                println!("step: {}, num molecules: {}", step, molecules.len());
            }
            let mut new_molecules: HashSet<String> = HashSet::new();
            for molecule in molecules {
                let individual_molecules = extract_molecules(&molecule)?;
                let transformed_molecules = self.step(individual_molecules);
                for m in transformed_molecules {
                    if m == target_molecule {
                        return Ok(step as u32);
                    } else if already_transformed.contains(&m) {
                        continue;
                    } else if m.len() < target_molecule.len() {
                        already_transformed.insert(m.clone());
                        new_molecules.insert(m);
                    }
                }
            }
            molecules = new_molecules;
        }
        unreachable!();
    }
}

fn extract_molecules(molecules_str: &str) -> Result<Vec<String>> {
    let mut molecules: Vec<String> = vec![];
    let mut chars = molecules_str.chars();
    let mut molecule = chars.next().context("Empty molecule")?.to_string();
    for c in chars {
        if c.is_uppercase() {
            molecules.push(molecule);
            molecule = String::new();
        }
        molecule.push(c);
    }
    molecules.push(molecule);
    Ok(molecules)
}

fn problem1(input: &str) -> Result<u32> {
    let (machine_str, molecule_str) = input.split_once("\n\n").context("Invalid puzzle input")?;
    let machine: Machine = machine_str.parse()?;
    let molecules = extract_molecules(molecule_str)?;
    Ok(machine.step(molecules).len() as u32)
}

fn problem2(input: &str) -> Result<u32> {
    let (machine_str, target_molecule) =
        input.split_once("\n\n").context("Invalid puzzle input")?;
    let machine: Machine = machine_str.parse()?;
    machine.make_medicine(target_molecule)
}

#[cfg(test)]
mod tests {
    use super::*;
    use anyhow::Result;

    #[test]
    fn test_problem1() -> Result<()> {
        let input = include_str!("../data/sample.txt").trim();
        let res = problem1(input)?;
        assert_eq!(res, 4);
        Ok(())
    }

    #[test]
    fn test_problem2() -> Result<()> {
        let input = include_str!("../data/sample.txt").trim();
        let res = problem2(input)?;
        assert_eq!(res, 3);
        Ok(())
    }

    #[test]
    fn test_extract_molecules() -> Result<()> {
        let input = "CRnSiRnCaP";
        let res = extract_molecules(input)?;
        assert_eq!(
            res,
            vec![
                "C".to_string(),
                "Rn".to_string(),
                "Si".to_string(),
                "Rn".to_string(),
                "Ca".to_string(),
                "P".to_string()
            ]
        );
        Ok(())
    }
}
