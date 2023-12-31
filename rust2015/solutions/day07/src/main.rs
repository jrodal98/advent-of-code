use std::collections::{HashMap, VecDeque};

fn main() {
    let input = include_str!("../data/input.txt").trim();
    println!("Problem 1: {}", problem1(input));
    println!("Problem 2: {}", problem2(input));
}

fn compute_answer(input: &str, b_override: Option<u16>) -> u16 {
    let mut signal_values = HashMap::new();
    if let Some(b) = b_override {
        signal_values.insert("b", b);
    }
    let mut queue: VecDeque<&str> = VecDeque::from(input.lines().collect::<Vec<&str>>());
    while let Some(line) = queue.pop_front() {
        let (input_logic, output_wire) = line.split_once(" -> ").unwrap();

        let tokens: Vec<&str> = input_logic.split_whitespace().collect();
        let output_signal = match tokens.len() {
            1 => {
                if let Ok(constant_signal) = tokens[0].parse::<u16>() {
                    Some(constant_signal)
                } else {
                    signal_values.get(tokens[0]).map(|v| *v)
                }
            }
            2 => signal_values.get(tokens[1]).map(|v| !v),
            3 => {
                if let Some(lv) = signal_values
                    .get(tokens[0])
                    .map(|v| *v)
                    .or_else(|| tokens[0].parse::<u16>().ok())
                {
                    match tokens[1] {
                        "AND" => signal_values.get(tokens[2]).map(|rv| lv & rv),
                        "OR" => signal_values.get(tokens[2]).map(|rv| lv | rv),
                        "LSHIFT" => Some(lv << tokens[2].parse::<u16>().unwrap()),
                        "RSHIFT" => Some(lv >> tokens[2].parse::<u16>().unwrap()),
                        _ => unreachable!(),
                    }
                } else {
                    None
                }
            }
            _ => unreachable!(),
        };
        if let Some(output_signal) = output_signal {
            if output_wire == "b" && b_override.is_some() {
                continue;
            }
            signal_values.insert(output_wire, output_signal);
        } else {
            queue.push_back(line);
        }
    }
    *signal_values.get("a").unwrap()
}

fn problem1(input: &str) -> u16 {
    compute_answer(input, None)
}

fn problem2(input: &str) -> u16 {
    compute_answer(input, Some(compute_answer(input, None)))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_problem1() {
        let input = include_str!("../data/sample.txt").trim();
        let res = problem1(input);
        assert_eq!(res, 114);
    }
}
