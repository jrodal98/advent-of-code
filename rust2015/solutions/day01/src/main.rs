fn main() {
    let input = include_str!("../data/input.txt");
    println!("Problem 1: {}", problem1(input));
    println!("Problem 2: {}", problem2(input));
}

fn problem1(input: &str) -> isize {
    input.chars().fold(0, |acc, c| {
        acc - match c {
            '(' => -1,
            ')' => 1,
            _ => unreachable!(),
        }
    })
}

fn problem2(input: &str) -> usize {
    let mut floor = 0;
    for (i, c) in input.chars().enumerate() {
        floor -= match c {
            '(' => -1,
            ')' => 1,
            _ => unreachable!(),
        };
        if floor == -1 {
            return i + 1;
        }
    }
    unreachable!();
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_problem1() {
        let input_solutions = vec![("(())", 0), ("()()", 0), ("(((", 3), ("(()(()(", 3)];
        for (input, solution) in input_solutions.into_iter() {
            let res = problem1(input);
            assert_eq!(res, solution);
        }
    }

    #[test]
    fn test_problem2() {
        let input_solutions = vec![(")", 1), ("()())", 5)];
        for (input, solution) in input_solutions.into_iter() {
            let res = problem2(input);
            assert_eq!(res, solution);
        }
    }
}
