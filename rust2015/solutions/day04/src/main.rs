fn main() {
    let input = include_str!("../data/input.txt").trim();
    println!("Problem 1: {}", problem1(input));
    println!("Problem 2: {}", problem2(input));
}

fn problem1(input: &str) -> u32 {
    let mut i = 0;
    loop {
        if &format!("{:x}", md5::compute(format!("{}{}", input, i)))[..5] == "00000" {
            return i;
        }
        i += 1;
    }
}

fn problem2(input: &str) -> u32 {
    let mut i = 0;
    loop {
        if &format!("{:x}", md5::compute(format!("{}{}", input, i)))[..6] == "000000" {
            return i;
        }
        i += 1;
    }
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
