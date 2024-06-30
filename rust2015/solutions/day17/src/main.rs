use anyhow::{Context, Result};
use std::collections::HashSet;

fn main() -> Result<()> {
    let input = include_str!("../data/input.txt").trim();
    println!("Problem 1: {}", problem1(input)?);
    println!("Problem 2: {}", problem2(input)?);
    Ok(())
}

fn do_the_thing(containers: Vec<u32>, remaining_liters: u32) -> u32 {
    let containers: Vec<u32> = containers
        .into_iter()
        .filter(|v| *v <= remaining_liters)
        .collect();

    let mut possible_paths = 0;
    for (i, &container) in containers.iter().enumerate() {
        if container == remaining_liters {
            possible_paths += 1;
        } else {
            possible_paths +=
                do_the_thing(containers[i + 1..].to_vec(), remaining_liters - container);
        }
    }
    possible_paths
}

fn problem1(input: &str) -> Result<u32> {
    let liters = if cfg!(test) { 25 } else { 150 };
    let containers = input
        .lines()
        .map(|line| {
            line.parse::<u32>()
                .context("Invalid input: Could not parse int")
        })
        .collect::<Result<Vec<_>, _>>()?;

    Ok(do_the_thing(containers, liters))
}

fn problem2(input: &str) -> Result<u32> {
    unimplemented!()
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
        assert_eq!(res, 0);
        Ok(())
    }
}
