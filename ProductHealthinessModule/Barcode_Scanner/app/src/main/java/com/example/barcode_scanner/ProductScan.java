package com.example.barcode_scanner;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.KeyEvent;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;

import java.util.Objects;

public class ProductScan extends AppCompatActivity implements View.OnClickListener {

    // variable for Text view.
    private TextView name;
    private TextView price;
    private TextView class_p;
    private TextView ingredient;
    private TextView allergen;
    private Button doneBtn;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_product_scan);

        // initializing our object class variable.
        name = findViewById(R.id.product_name);
        price = findViewById(R.id.product_price);
        class_p = findViewById(R.id.product_class);
        ingredient = findViewById(R.id.product_ingredient);
        allergen = findViewById(R.id.product_allergen);

        doneBtn = findViewById(R.id.doneBtn);
        doneBtn.setOnClickListener((View.OnClickListener) this);

        // create the get Intent object
        Intent intent = getIntent();
        // receive the value by getStringExtra() method and
        // key must be same which is send by first activity
        String nameD = intent.getStringExtra("name");
        String priceD = intent.getStringExtra("price");
        String classD = intent.getStringExtra("class");
        String ingredientD = intent.getStringExtra("ingredient");
        String allergenD = intent.getStringExtra("allergen");

        name.setText(nameD);
        price.setText(priceD);
        class_p.setText(classD);
        ingredient.setText(ingredientD);
        allergen.setText(allergenD);

    }

    @Override
    public void onClick(View view)
    {
        Intent intent = new Intent (ProductScan.this, MainActivity.class);
        startActivity(intent);finish();
    }

    @Override
    public void onBackPressed(){
        Toast.makeText(getApplicationContext(),"You Are Not Allowed to Exit the App", Toast.LENGTH_SHORT).show();
    }

    @Override
    public boolean onKeyDown(int keyCode, KeyEvent event) {
        if (keyCode == KeyEvent.KEYCODE_HOME) {
            Log.i("TEST", "Home Button");  // here you'll have to do something to prevent the button to go to the home screen
            return true;
        }
        return super.onKeyDown(keyCode, event);
    }
}
