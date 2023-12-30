fn main() {
    let input = include_str!("../data/input.txt");
    println!("Problem 1: {}", problem1(input));
    println!("Problem 2: {}", problem2(input));
}

fn problem1(input: &str) -> u32 {
    unimplemented!()
}

fn problem2(input: &str) -> u32 {
    unimplemented!()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_problem1() {
        let input = include_str!("../data/sample.txt");
        let res = problem1(input);
        assert_eq!(res, PART1_SAMPLE_SOLUTION);
    }

    #[test]
    fn test_problem2() {
        let input = include_str!("../data/sample.txt");
        let res = problem2(input);
        assert_eq!(res, 0);
    }
}
