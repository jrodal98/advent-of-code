use std::cmp::min;

fn main() {
    let input = include_str!("../data/input.txt");
    println!("Problem 1: {}", problem1(input));
    println!("Problem 2: {}", problem2(input));
}

fn problem1(input: &str) -> u32 {
    input
        .lines()
        .map(|line| {
            let dimensions: Vec<u32> = line.splitn(3, 'x').map(|d| d.parse().unwrap()).collect();
            let (l, w, h) = (dimensions[0], dimensions[1], dimensions[2]);
            let (s1, s2, s3) = (l * w, l * h, w * h);
            2 * (s1 + s2 + s3) + min(min(s1, s2), s3)
        })
        .sum()
}

fn problem2(input: &str) -> u32 {
    input
        .lines()
        .map(|line| {
            let dimensions: Vec<u32> = line.splitn(3, 'x').map(|d| d.parse().unwrap()).collect();
            let (l, w, h) = (dimensions[0], dimensions[1], dimensions[2]);
            let (p1, p2, p3) = (l + w, l + h, w + h);
            2 * min(min(p1, p2), p3) + l * w * h
        })
        .sum()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_problem1() {
        let input = include_str!("../data/sample.txt");
        let res = problem1(input);
        assert_eq!(res, 58);
    }

    #[test]
    fn test_problem2() {
        let input = include_str!("../data/sample.txt");
        let res = problem2(input);
        assert_eq!(res, 34);
    }
}
