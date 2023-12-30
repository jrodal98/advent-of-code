fn main() {
    let input = include_str!("../data/input.txt").trim();
    println!("Problem 1: {}", problem1(input));
    println!("Problem 2: {}", problem2(input));
}

fn problem1(input: &str) -> u32 {
    let mut lights = vec![vec![false; 1000]; 1000];
    for line in input.lines() {
        let (instruction_and_start, end) = line.split_once(" through ").unwrap();
        let (instruction, start) = instruction_and_start.rsplit_once(" ").unwrap();
        let (start_x, start_y): (usize, usize) = start
            .split_once(",")
            .map(|(x, y)| (x.parse().unwrap(), y.parse().unwrap()))
            .unwrap();
        let (end_x, end_y): (usize, usize) = end
            .split_once(",")
            .map(|(x, y)| (x.parse().unwrap(), y.parse().unwrap()))
            .unwrap();

        match instruction {
            "turn on" => {
                for x in start_x..=end_x {
                    for y in start_y..=end_y {
                        lights[y][x] = true;
                    }
                }
            }
            "turn off" => {
                for x in start_x..=end_x {
                    for y in start_y..=end_y {
                        lights[y][x] = false;
                    }
                }
            }
            "toggle" => {
                for x in start_x..=end_x {
                    for y in start_y..=end_y {
                        lights[y][x] = !lights[y][x];
                    }
                }
            }
            _ => unreachable!(),
        };
    }
    lights.into_iter().flatten().filter(|v| *v).count() as u32
}

fn problem2(input: &str) -> u32 {
    let mut lights = vec![vec![0; 1000]; 1000];
    for line in input.lines() {
        let (instruction_and_start, end) = line.split_once(" through ").unwrap();
        let (instruction, start) = instruction_and_start.rsplit_once(" ").unwrap();
        let (start_x, start_y): (usize, usize) = start
            .split_once(",")
            .map(|(x, y)| (x.parse().unwrap(), y.parse().unwrap()))
            .unwrap();
        let (end_x, end_y): (usize, usize) = end
            .split_once(",")
            .map(|(x, y)| (x.parse().unwrap(), y.parse().unwrap()))
            .unwrap();

        match instruction {
            "turn on" => {
                for x in start_x..=end_x {
                    for y in start_y..=end_y {
                        lights[y][x] += 1;
                    }
                }
            }
            "turn off" => {
                for x in start_x..=end_x {
                    for y in start_y..=end_y {
                        if lights[y][x] > 0 {
                            lights[y][x] -= 1;
                        }
                    }
                }
            }
            "toggle" => {
                for x in start_x..=end_x {
                    for y in start_y..=end_y {
                        lights[y][x] += 2;
                    }
                }
            }
            _ => unreachable!(),
        };
    }
    lights.into_iter().flatten().sum()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_problem1() {
        let input = include_str!("../data/sample.txt").trim();
        let res = problem1(input);
        assert_eq!(res, 998996);
    }
}
