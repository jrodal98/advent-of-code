use std::collections::HashMap;

use itertools::Itertools;

fn main() {
    let input = include_str!("../data/input.txt").trim();
    println!("Problem 1: {}", problem1(input));
    println!("Problem 2: {}", problem2(input));
}

fn problem1(input: &str) -> i32 {
    solve(input, None)
}

fn problem2(input: &str) -> i32 {
    solve(input, Some("Jacob"))
}

fn solve(input: &str, bonus_name: Option<&str>) -> i32 {
    let graph = parse_graph(input, bonus_name);
    let names = graph.keys().collect_vec();
    let mut answer = i32::MIN;
    for seats in names.iter().permutations(names.len()).unique() {
        answer = std::cmp::max(answer, score_seating(&graph, seats));
    }
    answer
}

fn parse_graph<'a>(
    input: &'a str,
    bonus_name: Option<&'a str>,
) -> HashMap<&'a str, HashMap<&'a str, i32>> {
    let mut graph: HashMap<&str, HashMap<&str, i32>> = HashMap::new();
    for line in input.lines() {
        let mut tokens = line.split_whitespace();
        let name1 = tokens.next().unwrap();
        let gain = tokens.nth(1).unwrap() == "gain";
        let units: i32 = tokens.next().unwrap().parse().unwrap();
        let name2 = tokens.last().unwrap().trim_end_matches(".");
        graph
            .entry(name1)
            .or_default()
            .insert(name2, if gain { units } else { -units });
        if let Some(name3) = bonus_name {
            graph.entry(name1).or_default().insert(name3, 0);
            graph.entry(name3).or_default().insert(name1, 0);
        }
    }
    graph
}

fn score_seating(graph: &HashMap<&str, HashMap<&str, i32>>, mut seats: Vec<&&&str>) -> i32 {
    seats.push(seats[0]);
    seats
        .windows(2)
        .map(|window| {
            let (name1, name2) = (*window[0], *window[1]);
            graph.get(name1).unwrap().get(name2).unwrap()
                + graph.get(name2).unwrap().get(name1).unwrap()
        })
        .sum()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_problem1() {
        let input = include_str!("../data/sample.txt").trim();
        let res = problem1(input);
        assert_eq!(res, 330);
    }
}
