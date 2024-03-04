package com.example.saimealert;

import static android.content.ContentValues.TAG;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.ImageView;
import android.widget.TextView;

import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;
import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.Date;

public class MainActivity extends AppCompatActivity {
    private DatabaseReference mDatabase;
    private TextView isSaimeAliveTV;
    private TextView lastVerifyTV;
    private TextView lastUpdateTV;
    private ImageView statusImage;
    private DateFormat formatter = new SimpleDateFormat("dd/MM/yyyy hh:mm:ss");


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        setContentView(R.layout.activity_main);
        getSupportActionBar().hide();
        isSaimeAliveTV = findViewById(R.id.status_textview);
        lastVerifyTV = findViewById(R.id.lastVerify_textview);
        lastUpdateTV = findViewById(R.id.lastUpdate_textview);
        statusImage = findViewById(R.id.saimedown_image);
        statusImage.setVisibility(View.INVISIBLE);
        mDatabase = FirebaseDatabase.getInstance().getReference();

        mDatabase.child("saime-status/").addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(@NonNull DataSnapshot dataSnapshot) {
                Boolean isSaimeAliveBool = dataSnapshot.child("isSaimeAlive").getValue(Boolean.class);

                Double verify = dataSnapshot.child("lastVerify").getValue(Double.class);
                Double update = dataSnapshot.child("lastUpdate").getValue(Double.class);

                Date lastVerify = new Date();
                Date lastUpdate = new Date();

                lastVerify.setTime((verify.longValue())*1000);
                lastUpdate.setTime((update.longValue())*1000);

                if(isSaimeAliveBool){
                    isSaimeAliveTV.setText("¡EL SAIME SE ENCUENTRA ARRIBA Y FUNCIONANDO!");
                    statusImage.setVisibility(View.INVISIBLE);
                }else{
                    isSaimeAliveTV.setText("¡EL SAIME SE ENCUENTRA CAÍDO!");
                    statusImage.setVisibility(View.VISIBLE);
                }
                lastVerifyTV.setText("Último chequeo: \n"+formatter.format(lastVerify));
                lastUpdateTV.setText("Última actualización en SAIME: \n"+formatter.format(lastUpdate));
                //lastVerifyTV.setText("Último chequeo: \n"+lastVerify.toString());
                //lastUpdateTV.setText("Última actualización en SAIME: \n"+lastUpdate.toString());
            }

            @Override
            public void onCancelled(DatabaseError error) {
                // Failed to read value
                Log.w(TAG, "Failed to read value.", error.toException());
            }
        });

    }

    @Override
    public void finish() {
        super.finish();
    }
}