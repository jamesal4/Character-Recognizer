//
//  RibbonViewController.swift
//  InertialMotion
//
//  Created by Justin Anderson on 3/17/17.
//  Copyright © 2017 MIT. All rights reserved.
//

import UIKit
import GLKit
import OpenGLES

class RibbonViewController: GLKViewController {

    // location and velocity renamed from Objective-C version to prevent property overloading error with Gesture3DViewController
    var ribbonLocation, ribbonVelocity: GLKVector3
    var pose: GLKQuaternion
    var context: EAGLContext?
    var ribbon: Ribbon?

    // MARK: - Lifecycle management for GLKViewController

    required init?(coder aDecoder: NSCoder) {
        ribbonLocation = GLKVector3()
        ribbonVelocity = GLKVector3()
        pose = GLKQuaternion()

        super.init(coder: aDecoder)
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        context = EAGLContext(api: .openGLES2)
        if (context == nil) {
            print("Failed to create ES context")
        }
        
        if let glkView = view as? GLKView,
            let context = context {
            glkView.context = context
            glkView.drawableDepthFormat = .format24
        }
        
        setupGL()
    }

    func setupGL() {
        EAGLContext.setCurrent(context)
        
        // Prepare the ribbon for drawing
        ribbon = Ribbon(lifetime: 20.0)
        ribbon?.setupGL()
    }
    
    func tearDownGL() {
        EAGLContext.setCurrent(context)
        
        // Free drawing resources used by the ribbon
        ribbon?.tearDownGL()
        ribbon = nil
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()

        if (isViewLoaded && view.window != nil) {
            view = nil
            tearDownGL()
            if (EAGLContext.current() == context) {
                EAGLContext.setCurrent(nil)
                context = nil
            }
        }
    }
    
    // MARK: - GLKView and GLKViewController delegate methods
    
    func update() {
        var modelViewMatrix = GLKMatrix4MakeWithQuaternion(GLKQuaternionInvert(pose))
        modelViewMatrix = GLKMatrix4TranslateWithVector3(modelViewMatrix, GLKQuaternionRotateVector3(pose, GLKVector3Make(0.0, 0.0, -0.3)))
        modelViewMatrix = GLKMatrix4TranslateWithVector3(modelViewMatrix, GLKVector3MultiplyScalar(ribbonLocation, -1))
        
        ribbon?.normalMatrix = GLKMatrix3InvertAndTranspose(GLKMatrix4GetMatrix3(modelViewMatrix), nil)
        
        let aspect = fabsf(Float(view.bounds.size.width / view.bounds.size.height))
        let projectionMatrix = GLKMatrix4MakePerspective(GLKMathDegreesToRadians(45.0), aspect, 0.1, 100.0)
        
        ribbon?.modelViewProjectionMatrix = GLKMatrix4Multiply(projectionMatrix, modelViewMatrix)
        
        ribbon?.advance(toTime: Date.timeIntervalSinceReferenceDate)
    }

    override func glkView(_ view: GLKView, drawIn rect: CGRect) {
        glClearColor(0, 0, 0, 1)
        glClear(GLenum(GL_COLOR_BUFFER_BIT) | GLenum(GL_DEPTH_BUFFER_BIT))
    
        ribbon?.draw()
    }

    // MARK: - Location update handling

    func appendPoint(_ point: GLKVector3, attitude: GLKQuaternion, draw: Bool) {
        pose = attitude
        ribbonLocation = point
        ribbon?.appendPoint(point,
                            attitude: attitude,
                            forTime: Date.timeIntervalSinceReferenceDate,
                            skip:!draw)
    }

    
    override var prefersStatusBarHidden: Bool {
        get {
            return true
        }
    }
}
