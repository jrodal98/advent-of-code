use std::str::FromStr;

use anyhow::{Context, Result};

fn main() -> Result<()> {
    let input = include_str!("../data/input.txt").trim();
    println!("Problem 1: {}", problem1(input)?);
    println!("Problem 2: {}", problem2(input)?);
    Ok(())
}

#[derive(Clone)]
struct Grid {
    rows: Vec<Vec<bool>>,
}

impl FromStr for Grid {
    type Err = anyhow::Error;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let rows = s
            .lines()
            .map(|line| line.chars().map(|c| c == '#').collect())
            .collect();
        Ok(Self { rows })
    }
}

impl Grid {
    fn step(&mut self) {
        let grid_copy = self.clone();
        let grid_size = grid_copy.rows.len();
        for row in 0..grid_size {
            for col in 0..grid_size {
                let cell = grid_copy.rows[row][col];
                let num_neighbors_on = vec![
                    row > 0 && col > 0 && grid_copy.rows[row - 1][col - 1],
                    row > 0 && grid_copy.rows[row - 1][col],
                    row > 0 && col + 1 < grid_size && grid_copy.rows[row - 1][col + 1],
                    col > 0 && grid_copy.rows[row][col - 1],
                    col + 1 < grid_size && grid_copy.rows[row][col + 1],
                    row + 1 < grid_size && col > 0 && grid_copy.rows[row + 1][col - 1],
                    row + 1 < grid_size && grid_copy.rows[row + 1][col],
                    row + 1 < grid_size && col + 1 < grid_size && grid_copy.rows[row + 1][col + 1],
                ]
                .into_iter()
                .filter(|v| *v)
                .count();
                self.rows[row][col] = (cell && (num_neighbors_on == 2 || num_neighbors_on == 3))
                    || (!cell && num_neighbors_on == 3);
            }
        }
    }
}

fn problem1(input: &str) -> Result<u32> {
    let steps = if cfg!(test) { 4 } else { 100 };
    let mut grid: Grid = input.parse()?;
    for _ in 0..steps {
        grid.step();
    }
    let num_cells_on = grid.rows.into_iter().flatten().filter(|v| *v).count();
    Ok(num_cells_on as u32)
}

fn problem2(input: &str) -> Result<u32> {
    Ok(0)
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
