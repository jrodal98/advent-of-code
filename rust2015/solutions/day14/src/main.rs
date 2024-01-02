use std::str::FromStr;

fn main() {
    let input = include_str!("../data/input.txt").trim();
    println!("Problem 1: {}", problem1(input, 2503));
    println!("Problem 2: {}", problem2(input, 2503));
}

struct Reindeer {
    speed: u32,
    stamina: u32,
    rest: u32,
}

impl Reindeer {
    pub fn fly(self, stop_time: u32) -> u32 {
        let full_cycles = stop_time / (self.stamina + self.rest);
        let partial_cycle = stop_time % (self.stamina + self.rest);
        full_cycles * (self.speed * self.stamina)
            + std::cmp::min(partial_cycle, self.stamina) * self.speed
    }
    pub fn fly_positions(self, stop_time: u32) -> Vec<u32> {
        let mut current_position = 0;
        let mut positions = vec![];
        for current_time in 0..stop_time {
            if current_time % (self.stamina + self.rest) < self.stamina {
                current_position += self.speed;
            }
            positions.push(current_position);
        }
        positions
    }
}

impl FromStr for Reindeer {
    type Err = ();

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let mut numbers = s.split_whitespace().filter_map(|token| token.parse().ok());
        Ok(Self {
            speed: numbers.next().unwrap(),
            stamina: numbers.next().unwrap(),
            rest: numbers.next().unwrap(),
        })
    }
}

fn problem1(input: &str, stop_time: u32) -> u32 {
    input
        .lines()
        .map(|line| Reindeer::from_str(line).unwrap().fly(stop_time))
        .max()
        .unwrap()
}

fn problem2(input: &str, stop_time: u32) -> u32 {
    let reindeer_positions: Vec<_> = input
        .lines()
        .map(|line| Reindeer::from_str(line).unwrap().fly_positions(stop_time))
        .collect();
    let mut reindeer_scores = vec![0; reindeer_positions.len()];
    for current_time in 0..stop_time as usize {
        let mut leading_reindeers = vec![];
        let mut leading_distance = u32::MIN;
        for (reindeer, positions) in reindeer_positions.iter().enumerate() {
            let reindeer_pos = positions[current_time];
            if reindeer_pos > leading_distance {
                leading_reindeers = vec![reindeer];
                leading_distance = reindeer_pos;
            } else if reindeer_pos == leading_distance {
                leading_reindeers.push(reindeer)
            }
        }
        for reindeer in leading_reindeers {
            reindeer_scores[reindeer] += 1;
        }
    }
    reindeer_scores.into_iter().max().unwrap()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_problem1() {
        let input = include_str!("../data/sample.txt").trim();
        let res = problem1(input, 1000);
        assert_eq!(res, 1120);
    }

    #[test]
    fn test_problem2() {
        let input = include_str!("../data/sample.txt").trim();
        let res = problem2(input, 1000);
        assert_eq!(res, 689);
    }
}
