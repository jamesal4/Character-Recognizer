//
//  LogNoteViewController.swift
//  InertialMotion
//
//  Created by Justin Anderson on 3/15/17.
//  Copyright © 2017 MIT. All rights reserved.
//

import UIKit

class LogNoteViewController: UIViewController {

    @IBOutlet weak var textView: UITextView?
    
    @IBAction func done(_ sender: Any) {
        let delegate: AppDelegate = UIApplication.shared.delegate as! AppDelegate
        if let entry = textView?.text {
            delegate.appendTrainingLog(entry: "\n\n\n\(entry)\n\n\n")
        }
        self.performSegue(withIdentifier: "exit", sender: sender)
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()

        // Do any additional setup after loading the view.
    }
    
    override func viewWillAppear(_ animated: Bool) {
        textView?.text = ""
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    

    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destinationViewController.
        // Pass the selected object to the new view controller.
    }
    */

}
