//
//  ColorInterpolator.swift
//  InertialMotion
//
//  Created by Justin Anderson on 3/16/17.
//  Copyright © 2017 MIT. All rights reserved.
//

import GLKit

@objc class ColorInterpolator: NSObject {
    var colors: [GLKVector3] = Array(repeating: GLKVector3Make(0, 0, 0), count: 2)
    var next_t: GLint = 0
    
    func pushColor(_ color: GLKVector3) {
        (colors[0], colors[1]) = (colors[1], color)
        next_t += 1
    }
    
    func colorForTime(_ t: Double) -> GLKVector3 {
        assert(next_t >= 2)
        assert(t >= Double(next_t - 2))
        assert(t <= Double(next_t - 1))
        let u = t - Double(next_t - 2)
        
        return GLKVector3Add(GLKVector3MultiplyScalar(colors[0], Float(u)), GLKVector3MultiplyScalar(colors[1], 1-Float(u)));
    }
}

@objc class ColorRandomizer: ColorInterpolator {
    func randomColor() -> GLKVector3 {
        let r = Float(ldexp(Double(arc4random()), -32))
        let g = Float(ldexp(Double(arc4random()), -32))
        let b = Float(ldexp(Double(arc4random()), -32))
        return GLKVector3Make(r, g, b)
    }
    
    @objc override func colorForTime(_ t: Double) -> GLKVector3 {
        if (next_t == 0) {
            next_t = GLint(t)
        }
        while (t > Double(next_t - 1)) {
            pushColor(randomColor())
        }
        return super.colorForTime(t)
    }
}
