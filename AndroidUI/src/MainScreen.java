package com.example.wildfiresmokedetection;

import androidx.appcompat.app.AppCompatActivity;

import android.app.ActionBar;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuInflater;

public class MainScreen extends AppCompatActivity {

    ActionBar menuBar;

    /*
      Created By: William Williams
      Created On: December 8th, 2019
      Purpose: Called when the user has inputted a correct username and password
               and the Activity is originally initiated.
      Actions Completed:
   */
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main_screen);
    }

    /*
      Created By: William Williams
      Created On: December 8th, 2019
      Purpose: Called when the user presses the back button on the navigation bar
      Actions Completed:
            - Does nothing to prevent going back to the login page.
   */
    @Override
    public void onBackPressed()
    {
        // Do nothing to prevent user from returning to the login page
    }

}
