use std::str::FromStr;

use anyhow::{Context, Result};

#[derive(Debug, PartialEq, Eq)]
struct Aunt {
    children: u32,
    cats: u32,
    samoyeds: u32,
    pomeranians: u32,
    akitas: u32,
    vizslas: u32,
    goldfish: u32,
    trees: u32,
    cars: u32,
    perfumes: u32,
}

impl Aunt {
    fn target_aunt() -> Self {
        Self {
            children: 3,
            cats: 7,
            samoyeds: 2,
            pomeranians: 3,
            akitas: 0,
            vizslas: 0,
            goldfish: 5,
            trees: 3,
            cars: 2,
            perfumes: 1,
        }
    }

    fn with_field(mut self, field: &str, value: u32) -> Self {
        match field {
            "children" => self.children = value,
            "cats" => self.cats = value,
            "samoyeds" => self.samoyeds = value,
            "pomeranians" => self.pomeranians = value,
            "akitas" => self.akitas = value,
            "vizslas" => self.vizslas = value,
            "goldfish" => self.goldfish = value,
            "trees" => self.trees = value,
            "cars" => self.cars = value,
            "perfumes" => self.perfumes = value,
            _ => panic!("Invalid field"),
        };
        self
    }
}

impl FromStr for Aunt {
    type Err = anyhow::Error;

    fn from_str(s: &str) -> Result<Self> {
        let aunt = Aunt::target_aunt();
        let (_, fields) = s
            .split_once(": ")
            .context("Invalid input: failed to parse fields")?;
        fields.split(", ").try_fold(aunt, |aunt, field_and_value| {
            let (field, value) = field_and_value
                .split_once(": ")
                .context("Invalid input: failed to parse field_and_value")?;
            Ok(aunt.with_field(
                field,
                value
                    .parse()
                    .context("Invalid input: failed to parse value into int")?,
            ))
        })
    }
}

fn main() -> Result<()> {
    let input = include_str!("../data/input.txt").trim();
    println!("Problem 1: {}", problem1(input)?);
    println!("Problem 2: {}", problem2(input)?);
    Ok(())
}

fn problem1(input: &str) -> Result<u32> {
    Ok(input
        .lines()
        .map(|line| line.parse::<Aunt>().unwrap())
        .enumerate()
        .find(|(_, aunt)| *aunt == Aunt::target_aunt())
        .unwrap()
        .0 as u32
        + 1)
}

fn problem2(input: &str) -> Result<u32> {
    unimplemented!()
}

#[cfg(test)]
mod tests {
    use super::*;
    use anyhow::Result;

    #[test]
    fn test_problem2() -> Result<()> {
        let input = include_str!("../data/sample.txt").trim();
        let res = problem2(input)?;
        assert_eq!(res, 0);
        Ok(())
    }
}
