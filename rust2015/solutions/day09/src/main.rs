use std::{
    collections::{HashMap, HashSet},
    ops::Deref,
};

fn main() {
    let input = include_str!("../data/input.txt").trim();
    println!("Problem 1: {}", problem1(input));
    println!("Problem 2: {}", problem2(input));
}

fn shortest_path<'a>(
    graph: &'a HashMap<&'a str, Vec<(&'a str, u32)>>,
    visited: &mut HashSet<&'a &'a str>,
    current_node: &'a &'a str,
    score: u32,
    best_score: u32,
) -> u32 {
    if score >= best_score {
        return u32::MAX;
    }

    if graph.len() == visited.len() {
        return score;
    }

    let mut best_score = best_score;
    for (next_node, weight) in graph.get(current_node).unwrap() {
        // already visited
        if !visited.insert(next_node) {
            continue;
        }
        // visit
        best_score = std::cmp::min(
            best_score,
            shortest_path(graph, visited, next_node, score + *weight, best_score),
        );
        // unvisit
        visited.remove(next_node);
    }
    best_score
}

fn problem1(input: &str) -> u32 {
    let mut graph: HashMap<&str, Vec<(&str, u32)>> = HashMap::new();
    for line in input.lines() {
        let mut tokens = line.split_whitespace();
        let from = tokens.next().unwrap();
        let to = tokens.nth(1).unwrap();
        let weight = tokens.last().unwrap().parse().unwrap();
        graph.entry(from).or_default().push((to, weight));
        graph.entry(to).or_default().push((from, weight));
    }
    let mut best_score = u32::MAX;
    for node in graph.keys() {
        let mut visited = HashSet::from([node]);
        best_score = shortest_path(&graph, &mut visited, node, 0, best_score);
    }
    best_score
}

fn problem2(input: &str) -> u32 {
    unimplemented!()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_problem1() {
        let input = include_str!("../data/sample.txt").trim();
        let res = problem1(input);
        assert_eq!(res, 605);
    }

    #[test]
    fn test_problem2() {
        let input = include_str!("../data/sample.txt").trim();
        let res = problem2(input);
        assert_eq!(res, 0);
    }
}
