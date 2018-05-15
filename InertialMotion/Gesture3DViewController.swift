//
//  Gesture3DViewController.swift
//  InertialMotion
//
//  Created by Justin Anderson on 3/15/17.
//  Copyright © 2017 MIT. All rights reserved.
//

import UIKit
import CoreMotion
import GLKit
import MessageUI

private func GLKQuaternionFromCMQuaternion(_ quat: CMQuaternion) -> GLKQuaternion {
    return GLKQuaternionMake(Float(quat.x), Float(quat.y), Float(quat.z), Float(quat.w))
}

private func GLKVector3FromCMAcceleration(_ acceleration: CMAcceleration) -> GLKVector3 {
    return GLKVector3Make(Float(acceleration.x), Float(acceleration.y), Float(acceleration.z))
}

class Gesture3DViewController: RibbonViewController, GestureProcessorDelegate, MFMailComposeViewControllerDelegate, UIPickerViewDelegate, UIPickerViewDataSource {

    @IBOutlet weak var recognizedLabel: UILabel?
    @IBOutlet weak var letterControl: UISegmentedControl!
    @IBOutlet weak var countLabel: UILabel!
    @IBOutlet weak var nameTextField: UITextField!
    @IBOutlet weak var letterTextField: UITextField!
    @IBOutlet weak var glkView: GLKView!
    
    var touchCount: Int = 0
    var letterCount = [String: Int]()
    var motionManager: CMMotionManager = CMMotionManager()
    var samples: [Sample3D] = []
    var position: GLKVector3 = GLKVector3()
    var velocity: GLKVector3 = GLKVector3()
    var logFile: FileHandle? = nil
    var alert: UIAlertController? = nil
    var logging: Bool = false
    let DATA_FILE_NAME = "log.csv"
    var LETTER: String = nil

    override func viewDidLoad() {
        super.viewDidLoad()
        
        // log file setup
        self.logFile = self.openFileForWriting()
        if self.logFile == nil {
            assert(false, "Couldn't open file for writing (" + self.getPathToLogFile() + ").")
        }
        self.logLineToDataFile("Time,Roll,Pitch,Yaw,AccelX,AccelY,AccelZ,Letter,Name\n")
        
        motionManager.deviceMotionUpdateInterval = 1e-2
        
        motionManager.startDeviceMotionUpdates(
            using: .xArbitraryCorrectedZVertical,
            to: OperationQueue.main) { [weak self] (motion, error) in
                self?.accumulateMotion(motion)
        }
        
        self.letterControl.addTarget(self, action:#selector(Gesture3DViewController.letterControlChanged(_:)), for: .valueChanged)
        
        self.countLabel.textColor = .white
        
        let datePicker = UIPickerView()
        datePicker.delegate = self
        datePicker.dataSource = self
        self.nameTextField.inputView = datePicker
    }
    
    @objc fileprivate func letterControlChanged(_ sender: UIDatePicker) {
        print("letter control changed")
        countLabel.text = "0"
    }
    
    override func viewDidAppear(_ animated: Bool) {
        becomeFirstResponder()
        samples.removeAll()
        
        let delegate = UIApplication.shared.delegate as! AppDelegate
        delegate.gestureProcessor.delegate = self

        super.viewDidAppear(animated)
    }
    
    func updateTouches(_ event: UIEvent?) {
        let touches = event?.allTouches?.filter({
            switch $0.phase {
            case .began, .moved, .stationary:
                return true
            default:
                return false
            }
        })
        touchCount = touches?.count ?? 0
    }
    
    override func touchesBegan(_ touches: Set<UITouch>, with event: UIEvent?) {
        updateTouches(event)
        logging = true
        print("touches began")
        self.glkView.backgroundColor = .green
    }
    
    override func touchesCancelled(_ touches: Set<UITouch>, with event: UIEvent?) {
        updateTouches(event)
    }
    
    override func touchesEnded(_ touches: Set<UITouch>, with event: UIEvent?) {
        updateTouches(event)
        logging = false
        let zero = String(0)
        let line = String.init(format: "%@,%@,%@,%@,%@,%@,%@,%@,%@\n", zero, zero, zero, zero, zero, zero, zero, zero, zero)
        logLineToDataFile(line)
        let curCount = Int(countLabel.text!)!
        countLabel.text = String(curCount+1)
        self.glkView.backgroundColor = .red
        print("touches ended")
        
    }
    
    func accumulateMotion(_ motion: CMDeviceMotion?) {
        if logging {
            guard let motion = motion else {
                return
            }
            
            let attitude = motion.attitude
            let userAcceleration = motion.userAcceleration
            
            let roll = String(attitude.roll)
            let pitch = String(attitude.pitch)
            let yaw = String(attitude.yaw)
            
            let accelX = String(userAcceleration.x)
            let accelY = String(userAcceleration.y)
            let accelZ = String(userAcceleration.z)
            
            LETTER = "something is wrong if you see this"
            switch self.letterControl.selectedSegmentIndex {
                case 0:
                    LETTER = "A"
                case 1:
                    LETTER = "B"
                case 2:
                    LETTER = "C"
                case 3:
                    LETTER = "D"
                case 4:
                    LETTER = "E"
                case 5:
                    LETTER = "V"
                case 6:
                    LETTER = "W"
                case 7:
                    LETTER = "X"
                case 8:
                    LETTER = "Y"
                case 9:
                    LETTER = "Z"
                default: ()
            }
            
            let name = nameTextField.text!
            
            let timeInterval = String(NSDate().timeIntervalSince1970)
            // write acceleration, timeInterval, and attitude to file
            let line = String.init(format: "%@,%@,%@,%@,%@,%@,%@,%@\n", timeInterval, roll, pitch, yaw, accelX, accelY, accelZ,letter,name)
            logLineToDataFile(line)
        }
    }
    
    func appendPoint(_ point: GLKVector3, attitude: GLKQuaternion) {
        let draw: Bool = touchCount > 0
        if draw {
            // Why is the z axis flipped?
            let position = GLKVector3Make(point.x, point.y, -point.z)
            let s = Sample3D(location: position,
                             attitude: attitude,
                             t: Date.timeIntervalSinceReferenceDate)
            samples.append(s)
        } else if (samples.count > 0) {
            let delegate = UIApplication.shared.delegate as! AppDelegate
            delegate.gestureProcessor.processGesture3D(samples: samples,
                                                       minSize: 0.01)
            samples.removeAll()
        }
        super.appendPoint(point, attitude: attitude, draw: draw)
    }
    
    func gestureProcessor(_ gestureProcessor: GestureProcessor, didRecognizeGesture label: String) {
        recognizedLabel?.text = recognizedLabel?.text?.appending(label)
    }
    
    func getPathToLogFile() -> String {
        let documentsPath = NSSearchPathForDirectoriesInDomains(.documentDirectory, .userDomainMask, true)[0]
        let filePath = documentsPath + "/" + DATA_FILE_NAME
        return filePath
    }
    
    func openFileForWriting() -> FileHandle? {
        let fileManager = FileManager.default
        let created = fileManager.createFile(atPath: self.getPathToLogFile(), contents: nil, attributes: nil)
        if !created {
            assert(false, "Failed to create file at " + self.getPathToLogFile() + ".")
        }
        return FileHandle(forWritingAtPath: self.getPathToLogFile())
    }
    
    func logLineToDataFile(_ line: String) {
        self.logFile?.write(line.data(using: String.Encoding.utf8)!)
        //print(line)
    }
    
    func resetLogFile() {
        self.logFile?.closeFile()
        self.logFile = self.openFileForWriting()
        if self.logFile == nil {
            assert(false, "Couldn't open file for writing (" + self.getPathToLogFile() + ").")
        }
    }
    
    @IBAction func emailLogFile(_ sender: UIButton) {
        if !MFMailComposeViewController.canSendMail() {
            self.alert = UIAlertController(title: "Can't send mail", message: "Please set up an email account on this phone to send mail", preferredStyle: UIAlertControllerStyle.alert)
            let ok = UIAlertAction(title: "OK", style: UIAlertActionStyle.default, handler: {(action:UIAlertAction) in
                self.dismiss(animated: true, completion: nil)
            })
            self.alert?.addAction(ok)
            self.present(self.alert!, animated: true, completion: nil)
            return
        } else {
            let fileData = NSData(contentsOfFile: self.getPathToLogFile())
            if fileData == nil || fileData?.length == 0 {
                return
            }
            let emailTitle = "0000000000000000000000000000000000"
            let messageBody = "Data from jim"
            let mc = MFMailComposeViewController()
            mc.mailComposeDelegate = self
            mc.setSubject(emailTitle)
            mc.setMessageBody(messageBody, isHTML: false)
            mc.addAttachmentData(fileData! as Data, mimeType: "text/plain", fileName: DATA_FILE_NAME)
            self.present(mc, animated: true, completion: nil)
        }
    }
    
    func mailComposeController(_ controller: MFMailComposeViewController, didFinishWith result: MFMailComposeResult, error: Error?) {
        controller.dismiss(animated: true, completion: nil)
    }
    
    @IBAction func hitClearButton(_ sender: UIButton) {
        self.resetLogFile()
    }
    
    func numberOfComponents(in pickerView: UIPickerView) -> Int {
        return 26
    }
    
    func pickerView(_ pickerView: UIPickerView, numberOfRowsInComponent component: Int) -> Int {
        return 1
    }
    
    func pickerView(_ pickerView: UIPickerView, titleForRow row: Int, forComponent component: Int) -> String? {
        return LETTERS[component]
    }
}
