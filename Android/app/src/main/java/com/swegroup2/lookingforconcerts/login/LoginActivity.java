package com.swegroup2.lookingforconcerts.login;

import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.AsyncTask;
import android.os.Bundle;
import android.preference.PreferenceManager;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import com.swegroup2.lookingforconcerts.R;
import com.swegroup2.lookingforconcerts.RefreshDto;
import com.swegroup2.lookingforconcerts.RefreshResponse;
import com.swegroup2.lookingforconcerts.RestInterfaceController;
import com.swegroup2.lookingforconcerts.concert.ConcertListActivity;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

/**
 * A login screen that offers login via username/password.
 */
public class LoginActivity extends AppCompatActivity {
    String username, password;
    String token;
    public static String refreshToken = "";
    public static String accessToken = "";


    // UI references.
    private EditText mUsernameView;
    private EditText mPasswordView;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        SharedPreferences settings = PreferenceManager
                .getDefaultSharedPreferences(getApplicationContext());
        token = settings.getString("token", null);


        username = "";
        password = "";
        // Set up the login form.
        mUsernameView = (EditText) findViewById(R.id.username);

        mPasswordView = (EditText) findViewById(R.id.password);

        if (token != null) {
            try {
                send();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }

        Button mEmailSignInButton = (Button) findViewById(R.id.email_sign_in_button);
        mEmailSignInButton.setOnClickListener(new OnClickListener() {
            @Override
            public void onClick(View view) {
                try {
                    send();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        });

        Button mEmailSignUpButton = (Button) findViewById(R.id.email_sign_up_button);
        mEmailSignUpButton.setOnClickListener(new OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(LoginActivity.this, SignupActivity.class);
                startActivity(intent);
            }
        });
    }


    private String convertStreamToString(InputStream is) {
        BufferedReader reader = new BufferedReader(new InputStreamReader(is));
        StringBuilder sb = new StringBuilder();

        String line = null;
        try {
            while ((line = reader.readLine()) != null) {
                sb.append(line).append('\n');
            }
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            try {
                is.close();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
        return sb.toString();
    }

    public static void refresh(final Context context) {
        Retrofit retrofit = new Retrofit.Builder()
                .baseUrl("http://34.210.127.92:8000/")
                .addConverterFactory(GsonConverterFactory.create())
                .build();

        RestInterfaceController controller = retrofit.create(RestInterfaceController.class);

        RefreshDto refreshDto = new RefreshDto();
        refreshDto.refresh = refreshToken;

        Call<RefreshResponse> call = controller.refresh(refreshDto);

        call.enqueue(new Callback<RefreshResponse>() {
            @Override
            public void onResponse(Call<RefreshResponse> call, Response<RefreshResponse> response) {
                if (!LoginActivity.accessToken.equals(response.body().access)) {
                    LoginActivity.accessToken = response.body().access;
                }
            }

            @Override
            public void onFailure(Call<RefreshResponse> call, Throwable t) {
                Toast.makeText(context, "ERROR", Toast.LENGTH_SHORT).show();
            }
        });
    }

    /**
     * Represents an asynchronous login/registration task used to authenticate
     * the user.
     */
    public class UserLoginTask extends AsyncTask<String, String, String> {

        private String message;
        Context mContext;

        UserLoginTask(Context context) {

            mContext = context;
        }

        @Override
        protected String doInBackground(String... params) {
            try {
                if (token == null) {
                    token = tryLogin(username, password);
                }

            } catch (Exception e) {
                e.printStackTrace();
                message = e.getMessage();
            }
            return message;
        }

        @Override
        protected void onPostExecute(String result) {
            if (token.equals("")) {
                Toast.makeText(mContext, "Wrong username or password!", Toast.LENGTH_LONG).show();
            } else {
                Intent i = new Intent(LoginActivity.this, ConcertListActivity.class);
                try {
                    JSONObject json = new JSONObject(token);
                    accessToken = json.getString("access");
                    refreshToken = json.getString("refresh");
                    SharedPreferences settings = PreferenceManager
                            .getDefaultSharedPreferences(getApplicationContext());
                    SharedPreferences.Editor editor = settings.edit();
                    editor.putString("token", token);
                    editor.commit();

                } catch (JSONException e) {
                    e.printStackTrace();
                }
                startActivity(i);
            }
        }

        @Override
        protected void onCancelled() {
        }
    }

    protected void send() throws MalformedURLException, IOException {
        username = mUsernameView.getText().toString();
        password = mPasswordView.getText().toString();

        new UserLoginTask(LoginActivity.this).execute();

    }

    protected String tryLogin(String username, String password) throws IOException {
        HttpURLConnection urlConnection = (HttpURLConnection) ((new URL("http://34.210.127.92:8000/api/auth/token/obtain/").openConnection()));
        String info = "{\n" +
                "\"username\":\"" + username + "\",\n" +
                "\"password\":\"" + password + "\"\n" +
                "\t\n" +
                "}\n" +
                "\n";
        String result = "";
        InputStream input = null;

        try {

            urlConnection.setDoOutput(true);
            urlConnection.setRequestProperty("Content-Type", "application/json");
            urlConnection.setRequestProperty("Accept", "application/json");

            urlConnection.setRequestMethod("POST");
            urlConnection.connect();

            OutputStream outputStream = urlConnection.getOutputStream();
            BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(outputStream, "UTF-8"));
            writer.write(info);
            writer.close();
            outputStream.close();
            if (urlConnection.getResponseCode() == 200) {
                input = urlConnection.getInputStream();
                result = convertStreamToString(input);

            } else {
            }

        } catch (Exception e) {
            e.printStackTrace();
        }
        return result;

    }


}
