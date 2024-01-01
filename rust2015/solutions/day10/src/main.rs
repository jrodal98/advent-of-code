fn main() {
    let input = include_str!("../data/input.txt").trim();
    println!("Problem 1: {}", solve(input, 40));
    println!("Problem 2: {}", solve(input, 50));
}

fn solve(input: &str, num_iterations: usize) -> usize {
    let mut answer_string = input.to_string();
    for _ in 0..num_iterations {
        let mut chars = answer_string.chars().peekable();
        let mut next_answer_string = String::new();
        while let Some(c) = chars.next() {
            let mut num_c = 1;
            while let Some(maybe_match) = chars.peek() {
                if maybe_match != &c {
                    break;
                }
                num_c += 1;
                chars.next();
            }
            next_answer_string.push(char::from_digit(num_c, 10).unwrap());
            next_answer_string.push(c);
        }
        answer_string = next_answer_string;
    }
    answer_string.len()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_problem1() {
        let input = include_str!("../data/sample.txt").trim();
        let res = solve(input, 1);
        assert_eq!(res, 6);
    }
}
