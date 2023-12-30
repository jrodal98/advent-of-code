fn main() {
    let input = include_str!("../data/input.txt").trim();
    println!("Problem 1: {}", problem1(input));
    println!("Problem 2: {}", problem2(input));
}

fn problem1(input: &str) -> u32 {
    let bad_doubles = vec!["ab", "cd", "pq", "xy"];
    let vowels = vec!['a', 'e', 'i', 'o', 'u'];
    input
        .lines()
        .filter(|line| {
            let mut num_vowels = 0;
            let mut duplicate_letter = false;
            let chars: Vec<char> = line.chars().collect();
            for i in 0..chars.len() - 1 {
                let c1 = chars[i];
                let c2 = chars[i + 1];
                if bad_doubles.contains(&format!("{}{}", c1, c2).as_str()) {
                    return false;
                }
                duplicate_letter = duplicate_letter || c1 == c2;
                if vowels.contains(&c1) {
                    num_vowels += 1;
                }
            }
            if vowels.contains(chars.last().unwrap()) {
                num_vowels += 1;
            }
            num_vowels >= 3 && duplicate_letter
        })
        .count() as u32
}

fn problem2(input: &str) -> u32 {
    input
        .lines()
        .filter(|line| {
            let mut has_pair = false;
            let mut has_repeat = false;
            let chars: Vec<char> = line.chars().collect();
            for i in 0..chars.len() - 1 {
                has_repeat = has_repeat || i < chars.len() - 2 && chars[i] == chars[i + 2];
                let pair = (chars[i], chars[i + 1]);
                if !has_pair {
                    for j in i + 2..chars.len() - 1 {
                        if (chars[j], chars[j + 1]) == pair {
                            has_pair = true;
                            break;
                        }
                    }
                }
                if has_pair && has_repeat {
                    break;
                }
            }
            has_pair && has_repeat
        })
        .count() as u32
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_problem1() {
        let input = include_str!("../data/sample.txt").trim();
        let res = problem1(input);
        assert_eq!(res, 2);
    }

    #[test]
    fn test_problem2() {
        let input = include_str!("../data/sample2.txt").trim();
        let res = problem2(input);
        assert_eq!(res, 2);
    }
}
