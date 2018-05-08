//
//  Gesture2DViewController.swift
//  InertialMotion
//
//  Created by Justin Anderson on 3/15/17.
//  Copyright © 2017 MIT. All rights reserved.
//

import UIKit

class Gesture2DViewController: UIViewController, GestureProcessorDelegate {

    @IBOutlet weak var recognizedLabel: UILabel?
    @IBOutlet weak var scribbleView: ScribbleView?
    @IBOutlet weak var longPressGestureRecognizer: UILongPressGestureRecognizer?

    private var samples: [Sample2D] = []
    
    @IBAction func longPress(_ sender: UILongPressGestureRecognizer) {
        if (self.presentedViewController == nil) {
            self.performSegue(withIdentifier: "logNote", sender: sender)
        }
    }
    
    @IBAction func prepareForUnwind(_ segue: UIStoryboardSegue) {
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        #if TRAINING
        // Note Swift doesn't support #define. To enable this, set a debug flag on the compiler (i.e. -D TRAINING)
        longPressGestureRecognizer?.isEnabled = true
        #else
        longPressGestureRecognizer?.isEnabled = false
        #endif
    }
    
    override func viewDidAppear(_ animated: Bool) {
        becomeFirstResponder()
        let delegate = UIApplication.shared.delegate as! AppDelegate
        delegate.gestureProcessor.delegate = self
        super.viewDidAppear(animated)
    }

    func updateTouches(_ event: UIEvent?) {
        var activeTouches: Set <UITouch> = Set()
        var cancelled: Bool = false

        // Unwrap optional NSSet <UITouch *>
        guard let allTouches = event?.allTouches else {
            print("No touches in touch event")
            return
        }
        for touch in allTouches {
            switch(touch.phase) {
            case .began, .moved, .stationary:
                activeTouches.insert(touch)
            case .cancelled:
                cancelled = true
                break
            default:
                break
            }
        }
        
        if (activeTouches.isEmpty == false) {
            let point: CGPoint = activeTouches.first!.location(in: view)
            let s = Sample2D(x: Double(point.x),
                             y: Double(point.y),
                             t: Date.timeIntervalSinceReferenceDate)
            samples.append(s)
            scribbleView?.add(point: point)
        } else if (!samples.isEmpty) {
            if (!cancelled) {
                print("Process gesture with \(samples.count) points")
                let delegate = UIApplication.shared.delegate as! AppDelegate
                delegate.gestureProcessor.processGesture2D(samples: samples, minSize: 100.0)
            }
            samples.removeAll()
            
            // Note Swift doesn't support #define. To enable this block, set a debug flag on the compiler (i.e. -D SCREENSHOT)
            #if SCREENSHOT
                UIGraphicsBeginImageContextWithOptions(UIScreen.main.bounds.size, false, UIScreen.main.scale)
                view.drawHierarchy(in: UIScreen.main.bounds, afterScreenUpdates: false)
                let image = UIGraphicsGetImageFromCurrentImageContext()
                UIImageWriteToSavedPhotosAlbum(image, nil, nil, nil)
                UIGraphicsEndImageContext()
            #endif
            
            scribbleView?.clear()
        }
    }

    override func touchesBegan(_ touches: Set<UITouch>, with event: UIEvent?) {
        updateTouches(event)
    }
    
    override func touchesCancelled(_ touches: Set<UITouch>, with event: UIEvent?) {
        updateTouches(event)
    }

    override func touchesEnded(_ touches: Set<UITouch>, with event: UIEvent?) {
        updateTouches(event)
    }
    
    override func touchesMoved(_ touches: Set<UITouch>, with event: UIEvent?) {
        updateTouches(event)
    }
    
    func gestureProcessor(_ gestureProcessor: GestureProcessor, didRecognizeGesture label: String) {
        // Note Swift doesn't support #define. To disable this block, set a debug flag on the compiler (i.e. -D SCREENSHOT)
        #if !SCREENSHOT
        recognizedLabel?.text = recognizedLabel?.text?.appending(label)
        #endif
    }

}
