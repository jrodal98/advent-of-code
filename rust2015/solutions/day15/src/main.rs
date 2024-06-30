use std::str::FromStr;

fn main() {
    let input = include_str!("../data/input.txt").trim();
    println!("Problem 1: {}", problem1(input));
    println!("Problem 2: {}", problem2(input));
}

struct Ingredient {
    name: String,
    capacity: i32,
    durability: i32,
    flavor: i32,
    texture: i32,
    calories: i32,
}

impl FromStr for Ingredient {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let (name, ingredients) = s.split_once(": ").unwrap();
        let properties: Vec<i32> = ingredients
            .split(", ")
            .map(|ingredient_with_property| {
                let (_, property_str) = ingredient_with_property.split_once(" ").unwrap();
                property_str.parse::<i32>().unwrap()
            })
            .collect();
        Ok(Self {
            name: name.to_string(),
            capacity: properties[0],
            durability: properties[1],
            flavor: properties[2],
            texture: properties[3],
            calories: properties[4],
        })
    }
}

impl Ingredient {
    fn score(ingredients: &[Self], amounts: &[u32], exact_calorie: Option<i32>) -> u32 {
        let mut capacity = 0;
        let mut durability = 0;
        let mut flavor = 0;
        let mut texture = 0;
        let mut calories = 0;

        for (ingredient, amount_u32) in ingredients.iter().zip(amounts) {
            let amount = *amount_u32 as i32;
            capacity += ingredient.capacity * amount;
            durability += ingredient.durability * amount;
            flavor += ingredient.flavor * amount;
            texture += ingredient.texture * amount;
            calories += ingredient.calories * amount;
        }

        if let Some(exact_calorie) = exact_calorie {
            if exact_calorie != calories {
                return 0;
            }
        }

        (capacity.max(0) * durability.max(0) * flavor.max(0) * texture.max(0)) as u32
    }
}

fn solve(input: &str, exact_calorie: Option<i32>) -> u32 {
    let ingredients: Vec<Ingredient> = input
        .lines()
        .map(|ingredient| ingredient.parse().unwrap())
        .collect();
    let mut score = 0;

    if ingredients.len() == 2 {
        for i in 0..=100 {
            score = score.max(Ingredient::score(
                &ingredients,
                &[i, 100 - i],
                exact_calorie,
            ));
        }
    } else {
        for a in 0..=100 {
            for b in 0..=100 - a {
                for c in 0..=100 - a - b {
                    let d = 100 - a - b - c;
                    score = score.max(Ingredient::score(
                        &ingredients,
                        &[a, b, c, d],
                        exact_calorie,
                    ));
                }
            }
        }
    }

    score
}

fn problem1(input: &str) -> u32 {
    solve(input, None)
}

fn problem2(input: &str) -> u32 {
    solve(input, Some(500))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_problem1() {
        let input = include_str!("../data/sample.txt").trim();
        let res = problem1(input);
        assert_eq!(res, 62842880);
    }

    #[test]
    fn test_problem2() {
        let input = include_str!("../data/sample.txt").trim();
        let res = problem2(input);
        assert_eq!(res, 57600000);
    }
}
