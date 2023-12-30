use std::collections::{HashMap, HashSet};

fn main() {
    let input = include_str!("../data/input.txt");
    println!("Problem 1: {}", problem1(input));
    println!("Problem 2: {}", problem2(input));
}

fn visited_points(input: &str) -> HashSet<(i32, i32)> {
    let mut visited = HashSet::new();
    let mut x = 0;
    let mut y = 0;
    visited.insert((x, y));
    for c in input.trim().chars() {
        match c {
            '>' => x += 1,
            '<' => x -= 1,
            '^' => y -= 1,
            'v' => y += 1,
            _ => unreachable!(),
        };
        visited.insert((x, y));
    }
    visited
}

fn problem1(input: &str) -> u32 {
    visited_points(input).len() as u32
}

fn problem2(input: &str) -> u32 {
    let mut s1 = String::new();
    let mut s2 = String::new();
    for (i, c) in input.trim().chars().enumerate() {
        if i % 2 == 0 {
            s1.push(c);
        } else {
            s2.push(c);
        }
    }
    visited_points(&s1)
        .union(&visited_points(&s2))
        .collect::<Vec<&(i32, i32)>>()
        .len() as u32
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_problem1() {
        let input = include_str!("../data/sample.txt");
        let res = problem1(input);
        assert_eq!(res, 2);
    }

    #[test]
    fn test_problem2() {
        let input = "^v^v^v^v^v";
        let res = problem2(input);
        assert_eq!(res, 11);
    }
}
