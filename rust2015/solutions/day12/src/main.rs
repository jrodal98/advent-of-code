use regex::Regex;

fn main() {
    let input = include_str!("../data/input.txt").trim();
    println!("Problem 1: {}", problem1(input));
    println!("Problem 2: {}", problem2(input));
}

fn problem1(input: &str) -> i64 {
    Regex::new(r"-?\d+")
        .unwrap()
        .find_iter(input)
        .map(|m| m.as_str().parse::<i64>().unwrap())
        .sum()
}

fn sum_of_object(value: &serde_json::Value) -> i64 {
    match value {
        serde_json::Value::Object(object) => {
            if object.values().any(|v| v.as_str() == Some("red")) {
                0
            } else {
                object.values().map(sum_of_object).sum()
            }
        }
        serde_json::Value::Array(array) => array.iter().map(sum_of_object).sum(),
        serde_json::Value::Number(n) => n.as_i64().unwrap_or(0),
        _ => 0,
    }
}

fn problem2(input: &str) -> i64 {
    sum_of_object(&serde_json::from_str(input).unwrap())
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
        let input = include_str!("../data/sample.txt").trim();
        let res = problem2(input);
        assert_eq!(res, 4);
    }
}
