use anyhow::Result;

fn main() -> Result<()> {
    let input = include_str!("../data/input.txt").trim();
    println!("Problem 1: {}", problem1(input)?);
    println!("Problem 2: {}", problem2(input)?);
    Ok(())
}

fn factors(n: usize) -> Vec<usize> {
    let mut result = Vec::new();
    let mut i = 1;
    while i * i <= n {
        if n % i == 0 {
            result.push(i);
            if i != n / i {
                result.push(n / i);
            }
        }
        i += 1;
    }
    result.sort();
    result
}

fn present_at_house(n: usize, is_part_1: bool) -> usize {
    let delivery_factor = if is_part_1 { 10 } else { 11 };
    factors(n)
        .iter()
        .filter(|e| is_part_1 || *e * 50 >= n)
        .map(|e| e * delivery_factor)
        .sum()
}

fn solve(input: &str, is_part_1: bool) -> Result<usize> {
    let target = input.parse::<usize>()?;
    for i in 1..target {
        if present_at_house(i, is_part_1) >= target {
            return Ok(i);
        }
    }
    Ok(target)
}

fn problem1(input: &str) -> Result<usize> {
    solve(input, true)
}

fn problem2(input: &str) -> Result<usize> {
    solve(input, false)
}

#[cfg(test)]
mod tests {
    use super::*;
    use anyhow::Result;

    #[test]
    fn test_problem1() -> Result<()> {
        let input = include_str!("../data/sample.txt").trim();
        let res = problem1(input)?;
        assert_eq!(res, 0);
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
