fn main() {
    let input = include_str!("../data/input.txt").trim();
    println!("Problem 1: {}", problem1(input));
    println!("Problem 2: {}", problem2(input));
}

fn is_valid_password(password: &str) -> bool {
    let mut chars: Vec<u8> = password
        .chars()
        .filter(|&c| c != 'i' && c != 'o' && c != 'l')
        .map(|c| c as u8)
        .collect();

    if chars.len() != password.len() {
        return false;
    }
    // dummy value to make windows work for 2 pair condition as well
    chars.push(0);
    let mut windows = chars.windows(3);
    let mut has_increasing_straight = false;
    let mut double_letters = 0;
    let mut last_pair = 0;
    while let Some(&[c1, c2, c3]) = windows.next() {
        has_increasing_straight = has_increasing_straight || (c1 + 1 == c2 && c2 + 1 == c3);
        if c1 == c2 && c1 != last_pair {
            double_letters += 1;
            last_pair = c1;
        } else {
            last_pair = 0;
        }
    }

    has_increasing_straight && double_letters > 1
}

fn increment_password(password: &str) -> String {
    let mut new_password_rev = Vec::with_capacity(password.len());
    let mut rev_chars = password.chars().rev();
    loop {
        let c = rev_chars.next().unwrap();
        let new_c = if c == 'z' { 'a' } else { (c as u8 + 1) as char };
        new_password_rev.push(new_c);
        if new_c != 'a' {
            new_password_rev.extend(rev_chars);
            break;
        }
    }
    new_password_rev.iter().rev().collect::<String>()
}

fn problem1(input: &str) -> String {
    let mut new_password = input.to_string();
    loop {
        new_password = increment_password(&new_password);
        if is_valid_password(&new_password) {
            return new_password;
        }
    }
}

fn problem2(input: &str) -> String {
    problem1(&problem1(input))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_problem1() {
        let input = include_str!("../data/sample.txt").trim();
        let res = problem1(input);
        assert_eq!(res, "ghjaabcc");
    }
}
