extern crate nalgebra as na;
extern crate rand;

use na::{DMat};
use rand::Rng;
use std::vec::Vec;
use std::ops::Mul;

fn outer<T>(vec_1:Vec<T>, vec_2:Vec<T>) -> DMat<T> 
    where T: Mul<Output=T> + Copy
{
   DMat::from_fn(vec_1.len(), vec_2.len(), |i, j| vec_1[i] * vec_2[j])
}

fn ising_gibbs(spins:usize) -> DMat<i64> {
    let blank = vec![0; spins];
    let ra_1 = blank.iter()
            .map(|_| rand::thread_rng().gen_range(0, 2))
            .collect::<Vec<_>>();
    let ra_2 = ra_1.clone();
    outer(ra_1, ra_2) 
}
fn main() {
    let iter = ising_gibbs(5);
    println!("{:?}", iter);
    //, beta:f64, field:f64, coupling:f64
}
