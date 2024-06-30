use std::str::FromStr;

use anyhow::{Context, Result};

#[derive(Debug, PartialEq, Eq, Default)]
struct Aunt {
    children: Option<u32>,
    cats: Option<u32>,
    samoyeds: Option<u32>,
    pomeranians: Option<u32>,
    akitas: Option<u32>,
    vizslas: Option<u32>,
    goldfish: Option<u32>,
    trees: Option<u32>,
    cars: Option<u32>,
    perfumes: Option<u32>,
}

impl Aunt {
    fn target_aunt() -> Self {
        Self {
            children: Some(3),
            cats: Some(7),
            samoyeds: Some(2),
            pomeranians: Some(3),
            akitas: Some(0),
            vizslas: Some(0),
            goldfish: Some(5),
            trees: Some(3),
            cars: Some(2),
            perfumes: Some(1),
        }
    }

    fn with_field(mut self, field: &str, value: u32) -> Self {
        match field {
            "children" => self.children = Some(value),
            "cats" => self.cats = Some(value),
            "samoyeds" => self.samoyeds = Some(value),
            "pomeranians" => self.pomeranians = Some(value),
            "akitas" => self.akitas = Some(value),
            "vizslas" => self.vizslas = Some(value),
            "goldfish" => self.goldfish = Some(value),
            "trees" => self.trees = Some(value),
            "cars" => self.cars = Some(value),
            "perfumes" => self.perfumes = Some(value),
            _ => panic!("Invalid field"),
        };
        self
    }

    fn is_target_aunt(&self, use_ranges: bool) -> bool {
        let target = Self::target_aunt();
        (self.children.is_none() || self.children == target.children)
            && (self.cats.is_none()
                || if use_ranges {
                    self.cats > target.cats
                } else {
                    self.cats == target.cats
                })
            && (self.samoyeds.is_none() || self.samoyeds == target.samoyeds)
            && (self.pomeranians.is_none()
                || if use_ranges {
                    self.pomeranians < target.pomeranians
                } else {
                    self.pomeranians == target.pomeranians
                })
            && (self.akitas.is_none() || self.akitas == target.akitas)
            && (self.vizslas.is_none() || self.vizslas == target.vizslas)
            && (self.goldfish.is_none()
                || if use_ranges {
                    self.goldfish < target.goldfish
                } else {
                    self.goldfish == target.goldfish
                })
            && (self.trees.is_none()
                || if use_ranges {
                    self.trees > target.trees
                } else {
                    self.trees == target.trees
                })
            && (self.cars.is_none() || self.cars == target.cars)
            && (self.perfumes.is_none() || self.perfumes == target.perfumes)
    }
}

impl FromStr for Aunt {
    type Err = anyhow::Error;

    fn from_str(s: &str) -> Result<Self> {
        let aunt = Aunt::default();
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

fn solve(input: &str, use_ranges: bool) -> Result<u32> {
    Ok(input
        .lines()
        .map(|line| line.parse::<Aunt>().expect("Failed to parse Aunt"))
        .enumerate()
        .find(|(_, aunt)| aunt.is_target_aunt(use_ranges))
        .context("Could not find target aunt")?
        .0 as u32
        + 1)
}

fn problem1(input: &str) -> Result<u32> {
    solve(input, false)
}

fn problem2(input: &str) -> Result<u32> {
    solve(input, true)
}
