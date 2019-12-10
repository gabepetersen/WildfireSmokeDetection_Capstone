/*
*   --File Name: LoginScreen.java
*   --Created By: William Williams
*   --Creation Date: December 5th, 2019
*   --Purpose: Initial activity when the user launches the application.
*      The User will have to either register their account, or login with already
*      created credentials.
*   --Associated Layout: layout/activity_login_screen.xml
 */

package com.example.wildfiresmokedetection;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.text.Editable;
import android.text.TextUtils;
import android.text.TextWatcher;
import android.view.View;
import android.view.Window;
import android.widget.Button;
import android.widget.EditText;

public class LoginScreen extends AppCompatActivity {

    private EditText usernameET, passwordET;
    private Button loginButton;

    /*
       Created By: William Williams
       Created On: December 5th, 2019
       Purpose: Called on Creation of the LoginScreen Activity.
       Actions Completed:
           -Sets the application to full screen, hiding the navigation bar.
               system bar, and application name.
           -Sets layout to login screen,
               layout file found at layout/activity_login_screen.xml
    */
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        //Hide the Application Name
        requestWindowFeature(Window.FEATURE_NO_TITLE);
        // Test to make sure that the android build number is at least KitKat
        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.KITKAT)
        {
            // Hides the Device's Navigation and Status Bars
            getWindow().getDecorView()
                    .setSystemUiVisibility(View.SYSTEM_UI_FLAG_LAYOUT_STABLE
                            | View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION
                            | View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN
                            | View.SYSTEM_UI_FLAG_HIDE_NAVIGATION
                            | View.SYSTEM_UI_FLAG_FULLSCREEN
                            | View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY
                    );
        }

        //Set content view to login screen layout
        setContentView(R.layout.activity_login_screen);

        // Reference to the login button on the layout, disable it at beginning
        loginButton = findViewById(R.id.login_button);
        loginButton.setEnabled(false);
        // Reference to username edit text box, attach text listener
        usernameET = findViewById(R.id.username_textEntry);
        usernameET.addTextChangedListener(loginWatcher);
        // Reference to password edit text box, attach text listener
        passwordET = findViewById(R.id.password_textEntry);
        passwordET.addTextChangedListener(loginWatcher);
    }

    /*
       Created By: William Williams
       Created On: December 5th, 2019
       Purpose: Called on resuming of the LoginScreen Activity.
       Actions Completed:
           -Sets the application to full screen, hiding the navigation bar.
               system bar, and application name.
    */
    @Override
    protected void onResume()
    {
        super.onResume();

        // Test to make sure that the android build number is at least KitKat
        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.KITKAT) {
            // Hides the Device's Navigation and Status Bars
            getWindow().getDecorView()
                    .setSystemUiVisibility(View.SYSTEM_UI_FLAG_LAYOUT_STABLE
                            | View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION
                            | View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN
                            | View.SYSTEM_UI_FLAG_HIDE_NAVIGATION
                            | View.SYSTEM_UI_FLAG_FULLSCREEN
                            | View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY
                    );
        }
    }

    /*
      Created By: William Williams
      Created On: December 5th, 2019
      Purpose: Called when the user has inputted a username and password
                and pressed the login button on the activity_login_screen.xml layout.
      Actions Completed:
            - Creates new Intent and starts the main activity page.
   */
    public void loginPressed(View v)
    {
        // Start the main page activity
        Intent startMainPage = new Intent(this, MainScreen.class);
        startActivity(startMainPage);
    }

    /*
     Created By: William Williams
     Created On: December 5th, 2019
     Purpose: Called when the user has inputted a username and password
               and pressed the login button on the activity_login_screen.xml layout.
     Actions Completed:
  */
    public void createAccount(View v)
    {
    }

    /*
     Created By: William Williams
     Created On: December 5th, 2019
     Purpose: Called when the user has inputted a username and password
               and pressed the login button on the activity_login_screen.xml layout.
     Actions Completed:
  */
    public void forgotUsernamePassword(View v)
    {
    }


    TextWatcher loginWatcher = new TextWatcher()
    {
        /*
        Created By: William Williams
        Created On: December 8th, 2019
        Purpose: Called when the user has modified text in the text box
        Actions Completed: Checks if either text box is empty for enabling login button
        */
        @Override
        public void onTextChanged(CharSequence s, int start, int before, int count)
        {
            if(TextUtils.isEmpty(usernameET.getText()) ||
                TextUtils.isEmpty(passwordET.getText()))
            {
                // If one of the text box's is empty, disable login button
                loginButton.setEnabled(false);
            }
            else
            {
                // If both text box's have content, enable login button.
                loginButton.setEnabled(true);
            }
        }

        @Override
        public void beforeTextChanged(CharSequence s, int start, int count, int after)
        {
        }

        @Override
        public void afterTextChanged(Editable s)
        {
        }
    };
}
