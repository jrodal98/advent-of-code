use anyhow::{Context, Result};
use std::str::FromStr;

fn main() -> Result<()> {
    let input = include_str!("../data/input.txt").trim();
    println!("Problem 1: {}", problem1(input)?);
    println!("Problem 2: {}", problem2(input)?);
    Ok(())
}

struct Ingredient {
    #[allow(dead_code)]
    name: String,
    capacity: i32,
    durability: i32,
    flavor: i32,
    texture: i32,
    calories: i32,
}

impl FromStr for Ingredient {
    type Err = anyhow::Error;

    fn from_str(s: &str) -> Result<Self> {
        let (name, ingredients) = s.split_once(": ").context("Invalid input format")?;
        let properties = ingredients
            .split(", ")
            .map(|ingredient_with_property| {
                let (_, property_str) = ingredient_with_property
                    .split_once(" ")
                    .context("Invalid property format")?;
                property_str.parse().context("Invalid number")
            })
            .collect::<Result<Vec<i32>>>()?;

        if properties.len() != 5 {
            return Err(anyhow::anyhow!("Invalid number of properties"));
        }

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
        let (mut capacity, mut durability, mut flavor, mut texture, mut calories) = (0, 0, 0, 0, 0);

        for (ingredient, &amount) in ingredients.iter().zip(amounts) {
            let amount = amount as i32;
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

fn solve(input: &str, exact_calorie: Option<i32>) -> Result<u32> {
    let ingredients: Vec<Ingredient> = input
        .lines()
        .map(|line| line.parse().context("Invalid ingredient format"))
        .collect::<Result<Vec<Ingredient>>>()?;
    let mut max_score = 0;

    match ingredients.len() {
        2 => {
            for i in 0..=100 {
                max_score = max_score.max(Ingredient::score(
                    &ingredients,
                    &[i, 100 - i],
                    exact_calorie,
                ));
            }
        }
        4 => {
            for a in 0..=100 {
                for b in 0..=100 - a {
                    for c in 0..=100 - a - b {
                        let d = 100 - a - b - c;
                        max_score = max_score.max(Ingredient::score(
                            &ingredients,
                            &[a, b, c, d],
                            exact_calorie,
                        ));
                    }
                }
            }
        }
        _ => return Err(anyhow::anyhow!("Unsupported number of ingredients")),
    }

    Ok(max_score)
}

fn problem1(input: &str) -> Result<u32> {
    solve(input, None)
}

fn problem2(input: &str) -> Result<u32> {
    solve(input, Some(500))
}

#[cfg(test)]
mod tests {
    use super::*;
    use anyhow::Result;

    #[test]
    fn test_problem1() -> Result<()> {
        let input = include_str!("../data/sample.txt").trim();
        let res = problem1(input)?;
        assert_eq!(res, 62842880);
        Ok(())
    }

    #[test]
    fn test_problem2() -> Result<()> {
        let input = include_str!("../data/sample.txt").trim();
        let res = problem2(input)?;
        assert_eq!(res, 57600000);
        Ok(())
    }
}
