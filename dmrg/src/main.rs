extern crate nalgebra;

use nalgebra::{DMat, DVec};
use std::ops::{Add, Sub, Mul};

trait Conjugable {
    fn conj(&self) -> Self;
}

impl Conjugable for f64 {
    fn conj(&self) -> f64 {
        *self
    }
}

#[derive(Debug, Clone)]
struct Operator<T: Mul + Add + Sub + Copy> {
    mat_rep: DMat<T>,
}

#[derive(Debug, Clone)]
struct Bra<T> 
    where T: Mul + Add + Sub + Copy
{  
    mat_rep : DVec<T>,
}

#[derive(Debug, Clone)]
struct Ket<T> 
    where T: Mul + Add + Sub + Copy
{
    mat_rep : DVec<T>,
}

impl<T> Mul<Operator<T>> for Bra<T>
    where T: Mul + Add + Sub + Copy
{
    type Output = Bra<T>;
    
    fn mul(self, f:Operator<T>) -> Bra<T> {
        Bra { mat_rep : self.mat_rep * f.mat_rep }
    }
}

impl<T> Mul<Ket<T>> for Operator<T>
    where T: Mul + Add + Sub + Copy
{
    type Output = Ket<T>;

    fn mul(self, f:Ket<T>) -> Ket<T> {
        Ket { mat_rep : self.mat_rep * f.mat_rep }
    }
}

impl<T> Mul<Operator<T>> for Operator<T>
    where T: Mul + Add + Sub + Copy
{
    type Output = Operator<T>;

    fn mul(self, f:Operator<T>) -> Operator<T> {
        Operator { mat_rep : self.mat_rep * f.mat_rep }
    }
}

impl<T> Mul<Ket<T>> for Bra<T>
    where T: Mul + Add + Sub + Copy + Conjugable
{
    type Output = T;

    fn mul(self, f:Ket<T>) -> T {
        let mut ret: T = 0.0;
        for (ai, bi) in self.mat_rep.zip(f.mat_rep) {
            ret += ai*bi;
        }
        ret
    }
}

fn main() {
    let op = Operator {mat_rep: DMat::from_fn(4, 4, |i, j| i as f64 + j as f64)};
    let st = Ket {mat_rep: DVec::from_fn(4, |i| i as f64)};
    println!("{:?}", op);
    println!("{:?}", st);

}
