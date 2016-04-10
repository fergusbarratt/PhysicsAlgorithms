extern crate gnuplot as gn;
extern crate nalgebra as na;
extern crate rand;

use na::{DMat};
use rand::Rng;
use std::vec::Vec;
use gn::{Figure, Caption, Color};

fn outer(vec_1:Vec<f64>, vec_2:Vec<f64>) -> DMat<f64> 
{
   DMat::from_fn(vec_1.len(), vec_2.len(), |i, j| vec_1[i] * vec_2[j])
}

fn hadamard(mat_1:DMat<f64>, mat_2:DMat<f64>) -> DMat<f64>
{
    let vec_1 = mat_1.clone().into_vec();
    let vec_2 = mat_2.clone().into_vec();
    let zip_ret_vec = vec_1.iter().zip(vec_2);
    let mut ret_vec: Vec<f64> = vec![];
    for tup in zip_ret_vec {
        ret_vec.push(tup.0*tup.1);
    }
    DMat::from_col_vec(mat_1.nrows(), mat_2.ncols(), &ret_vec) 
}

// fn mat_sum_no_diag(mat:DMat<f64>) -> f64 
// {
//     let rem_diag = DMat::from_fn(mat.nrows(), mat.ncols(), |i, j| if i==j {0.0} else {1.0});
//     mat_sum(hadamard(mat, rem_diag))
// }

fn mat_sum(mat:DMat<f64>) -> f64 
{
    mat.into_vec().iter().fold(0.0, |sum, x| sum + x)
}

fn spin_sum(vec:Vec<f64>) -> f64 
{
    vec.iter().fold(0.0, |sum, x| sum + x) 
}

fn rand_spin_chain(spins:usize) -> Vec<f64> 
{
    let blank = vec![0; spins];
    blank.iter()
            .map(|_| rand::thread_rng().gen_range(0, 2) as f64)
            .collect::<Vec<_>>()
}

fn ham(coupling:DMat<f64>, beta:f64, h:f64, spins:usize) -> f64
{
    let s_c = rand_spin_chain(spins);
    let quad = beta * mat_sum(hadamard(coupling, outer(s_c.clone(), s_c.clone())));
    let vec = h *  spin_sum(s_c.clone());
    quad + vec
}

fn main() 
{
    let size:usize = 10;
    let coupling = DMat::from_fn(size, size, |i, j| if i == j {0.0} else{1.0}); 
    let mut hams:Vec<f64> = vec![];
    let x = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]; 
    for h in x.iter() {
      hams.push(ham(coupling.clone(), *h, 1.0, size));
    }

    let mut fg = Figure::new();
    fg.axes2d()
      .lines(&x, &hams, &[Caption("A line"), Color("black")]);
    fg.show();
}
