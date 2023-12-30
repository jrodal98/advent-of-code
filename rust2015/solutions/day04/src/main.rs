fn main() {
    let input = include_str!("../data/input.txt").trim();
    println!("Problem 1: {}", problem1(input));
    println!("Problem 2: {}", problem2(input));
}

fn find_hash_with_leading_zeros(input: &str, num_zeros: usize) -> u32 {
    let mut i = 0;
    let target = "0".repeat(num_zeros);
    loop {
        if &format!("{:x}", md5::compute(format!("{}{}", input, i)))[..num_zeros] == target {
            return i;
        }
        i += 1;
    }
}

fn problem1(input: &str) -> u32 {
    find_hash_with_leading_zeros(input, 5)
}

fn problem2(input: &str) -> u32 {
    find_hash_with_leading_zeros(input, 6)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_problem1() {
        let input = include_str!("../data/sample.txt").trim();
        let res = problem1(input);
        assert_eq!(res, 609043);
    }
}
