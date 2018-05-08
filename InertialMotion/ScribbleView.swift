//
//  ScribbleView.swift
//  InertialMotion
//
//  Created by Justin Anderson on 3/16/17.
//  Copyright © 2017 MIT. All rights reserved.
//

import UIKit

class ScribbleView: UIView {

    private var path: UIBezierPath = UIBezierPath()
    private let color: UIColor = #colorLiteral(red: 0, green: 0, blue: 0, alpha: 1)
    private var recentPoints: [CGPoint] = [.zero, .zero]
    private var pointCount: Int = 0
    
    
    required init?(coder aDecoder: NSCoder) {
        path.lineWidth = 10.0
        path.lineCapStyle = .round
        path.lineJoinStyle = .round

        super.init(coder: aDecoder)
    }
    
    override func draw(_ rect: CGRect) {
        color.setStroke()
        path.stroke()
    }
    
    func add(point: CGPoint) {
        switch pointCount {
        case 0:
            path.move(to: point)
        case 1:
            path.addLine(to: point)
        default:
            let velocity = CGPoint(x: (point.x - recentPoints[0].x) * 0.5,
                                   y: (point.y - recentPoints[0].y) * 0.5)
            let control = CGPoint(x: recentPoints[1].x + 0.5 * velocity.x,
                                  y: recentPoints[1].y + 0.5 * velocity.y)
            path.addQuadCurve(to: point, controlPoint: control)
        }
        
        (recentPoints[0], recentPoints[1]) = (recentPoints[1], point)
        pointCount += 1;
        
        setNeedsDisplay()
    }
    
    func clear() {
        path.removeAllPoints()
        pointCount = 0
        setNeedsDisplay()
    }
}
