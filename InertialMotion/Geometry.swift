//
//  Geometry.swift
//  InertialMotion
//
//  Created by Justin Anderson on 3/15/17.
//  Copyright © 2017 MIT. All rights reserved.
//

import Foundation
import GLKit
import Accelerate

enum GeometryError: Error {
    case matrixException(String)
}

func nearestRotation(_ input: GLKMatrix3) throws -> GLKMatrix3 {
    // Heavily modified from code by Luke Lonergan, under the license "Use pfreely".
    var jobz = Int8(UnicodeScalar("A").value)
    var A: [Double] = Array(repeating: 0.0, count: 9)
    var S: [Double] = Array(repeating: 0.0, count: 3)
    var U: [Double] = Array(repeating: 0.0, count: 9)
    var Vt: [Double] = Array(repeating: 0.0, count: 9)

    for j in 0..<3 {
        for i in 0..<3 {
            A[j+i*3] = Double(input[i+j*3]);
        }
    }
    
    // compute singular value decomposition of A in column-major order
    var iwork: [__CLPK_integer] = Array.init(repeating: 0, count: 24)
    var n, lwork, info: __CLPK_integer
    var dwork: Double
    n = 3
    lwork = -1
    info = -1
    dwork = 0
    
    dgesdd_(&jobz, &n, &n, &A, &n, &S, &U, &n, &Vt, &n, &dwork, &lwork, &iwork, &info);
    if (info != 0) {
        throw GeometryError.matrixException("Error while performing SVD")
    }
    lwork = __CLPK_integer(dwork)
    var work: [Double] = Array(repeating: 0.0, count: Int(lwork))
    dgesdd_(&jobz, &n, &n, &A, &n, &S, &U, &n, &Vt, &n, &work, &lwork, &iwork, &info);
    if (info != 0) {
        throw GeometryError.matrixException("Error while performing SVD")
    }
    
    // compute nearest rotation to input
    // we're ignoring a subtlety having to do with the sign of the determinant
    // GLKMatrix3 is immutable in Swift, so we'll build it in one shot after gathering all values.
    var m: [Float] = Array.init(repeating: 0.0, count: 9)
    for i in 0..<3 {
        for j in 0..<3 {
            m[i*3+j] = Float(Vt[0+i*3] * U[j+0*3] + Vt[1+i*3] * U[j+1*3] + Vt[2+i*3] * U[j+2*3])
        }
    }
    
    return GLKMatrix3(m: (m[0], m[1], m[2], m[3], m[4], m[5], m[6], m[7], m[8]))
}
