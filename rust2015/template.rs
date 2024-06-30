use anyhow::{Context, Result};

fn main() -> Result<()> {
    let input = include_str!("../data/input.txt").trim();
    println!("Problem 1: {}", problem1(input)?);
    println!("Problem 2: {}", problem2(input)?);
    Ok(())
}

fn problem1(input: &str) -> Result<u32> {
    unimplemented!()
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
        assert_eq!(res, PART1_SAMPLE_SOLUTION);
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
