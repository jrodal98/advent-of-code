use anyhow::{Context, Result};

fn main() -> Result<()> {
    let input = include_str!("../data/input.txt").trim();
    println!("Problem 1: {}", problem1(input)?);
    println!("Problem 2: {}", problem2(input)?);
    Ok(())
}

fn get_possible_paths_helper(
    containers: Vec<u32>,
    path_length: u32,
    remaining_liters: u32,
) -> Vec<u32> {
    let containers: Vec<u32> = containers
        .into_iter()
        .filter(|v| *v <= remaining_liters)
        .collect();

    let mut possible_paths: Vec<u32> = vec![];
    for (i, &container) in containers.iter().enumerate() {
        if container == remaining_liters {
            possible_paths.push(path_length + 1);
        } else {
            possible_paths.extend(get_possible_paths_helper(
                containers[i + 1..].to_vec(),
                path_length + 1,
                remaining_liters - container,
            ))
        }
    }
    possible_paths
}

fn get_possible_paths(input: &str) -> Result<Vec<u32>> {
    let liters = if cfg!(test) { 25 } else { 150 };
    let containers = input
        .lines()
        .map(|line| {
            line.parse::<u32>()
                .context("Invalid input: Could not parse int")
        })
        .collect::<Result<Vec<_>, _>>()?;
    Ok(get_possible_paths_helper(containers, 0, liters))
}

fn problem1(input: &str) -> Result<u32> {
    get_possible_paths(input).map(|paths| paths.len() as u32)
}

fn problem2(input: &str) -> Result<u32> {
    let possible_paths = get_possible_paths(input)?;
    let mut num_min_paths = 0;
    let mut min_path_length = u32::MAX;
    for path_length in possible_paths {
        if path_length < min_path_length {
            num_min_paths = 1;
            min_path_length = path_length;
        } else if path_length == min_path_length {
            num_min_paths += 1;
        }
    }
    Ok(num_min_paths)
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
}
