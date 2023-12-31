fn main() {
    let input = include_str!("../data/input.txt").trim();
    println!("Problem 1: {}", problem1(input));
    println!("Problem 2: {}", problem2(input));
}

fn problem1(input: &str) -> u32 {
    input
        .lines()
        .map(|line| {
            let mut chars = line[1..line.len() - 1].chars();
            let mut num_special = 2;
            while let Some(c) = chars.next() {
                if c != '\\' {
                    continue;
                }
                match chars.next().unwrap() {
                    '\\' | '"' => {
                        num_special += 1;
                    }
                    'x' => {
                        chars.nth(1); // consume 2 chars after x
                        num_special += 3;
                    }
                    _ => unreachable!(),
                };
            }
            num_special
        })
        .sum()
}

fn problem2(input: &str) -> u32 {
    input
        .lines()
        .map(|line| line.chars().filter(|&c| c == '\\' || c == '"').count() as u32 + 2)
        .sum()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_problem1() {
        let input = include_str!("../data/sample.txt").trim();
        let res = problem1(input);
        assert_eq!(res, 12);
    }

    #[test]
    fn test_problem2() {
        let input = include_str!("../data/sample.txt").trim();
        let res = problem2(input);
        assert_eq!(res, 19);
    }
}
