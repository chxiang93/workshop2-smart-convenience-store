package com.example.barcode_scanner;

import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;

import android.Manifest;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.media.AudioManager;
import android.media.ToneGenerator;
import android.os.Bundle;
import android.util.Log;
import android.util.SparseArray;
import android.view.KeyEvent;
import android.view.SurfaceHolder;
import android.view.SurfaceView;
import android.widget.TextView;
import android.widget.Toast;

import com.google.android.gms.vision.CameraSource;
import com.google.android.gms.vision.Detector;
import com.google.android.gms.vision.barcode.Barcode;
import com.google.android.gms.vision.barcode.BarcodeDetector;
import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;

import java.io.IOException;
import java.util.Objects;

public class MainActivity extends AppCompatActivity {


    private SurfaceView surfaceView;
    private BarcodeDetector barcodeDetector;
    private CameraSource cameraSource;
    private static final int REQUEST_CAMERA_PERMISSION = 201;
    private ToneGenerator toneGen1;
    private TextView barcodeText;
    private String barcodeData;

    String dbName;
    String dbPrice;
    String dbClass;
    String dbAllergen;
    String dbIngredient;



    // creating a variable for
    // our Firebase Database.
    FirebaseDatabase firebaseDatabase;

    // creating a variable for our
    // Database Reference for Firebase.
    DatabaseReference databaseReference;
    String m_name = "",m_price = "",m_class = "",m_allergen ="",m_ingredient = "";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        toneGen1 = new ToneGenerator(AudioManager.STREAM_MUSIC, 100);
        surfaceView = findViewById(R.id.surface_view);
        barcodeText = findViewById(R.id.barcode_text);
        initialiseDetectorsAndSources();

        // below line is used to get the instance
        // of our Firebase database.
        firebaseDatabase = FirebaseDatabase.getInstance("https://conveniencestore-c5795-default-rtdb.asia-southeast1.firebasedatabase.app");

        // below line is used to get
        // reference for our database.
        databaseReference = firebaseDatabase.getReference("Barcodes");

        //reference = FirebaseDatabase.getInstance().getReference("students");
    }

    private void initialiseDetectorsAndSources() {

        //Toast.makeText(getApplicationContext(), "Barcode scanner started", Toast.LENGTH_SHORT).show();

        barcodeDetector = new BarcodeDetector.Builder(this)
                .setBarcodeFormats(Barcode.ALL_FORMATS)
                .build();

        cameraSource = new CameraSource.Builder(this, barcodeDetector)
                .setRequestedPreviewSize(1920, 1080)
                .setAutoFocusEnabled(true) //you should add this feature
                .setFacing(CameraSource.CAMERA_FACING_FRONT)
                .build();

        surfaceView.getHolder().addCallback(new SurfaceHolder.Callback() {
            @Override
            public void surfaceCreated(SurfaceHolder holder) {
                try {
                    if (ActivityCompat.checkSelfPermission(MainActivity.this, Manifest.permission.CAMERA) == PackageManager.PERMISSION_GRANTED) {
                        cameraSource.start(surfaceView.getHolder());
                    } else {
                        ActivityCompat.requestPermissions(MainActivity.this, new
                                String[]{Manifest.permission.CAMERA}, REQUEST_CAMERA_PERMISSION);
                    }

                } catch (IOException e) {
                    e.printStackTrace();
                }


            }

            @Override
            public void surfaceChanged(SurfaceHolder holder, int format, int width, int height) {
            }

            @Override
            public void surfaceDestroyed(SurfaceHolder holder) {
                cameraSource.stop();
            }
        });


        barcodeDetector.setProcessor(new Detector.Processor<Barcode>() {
            @Override
            public void release() {
                // Toast.makeText(getApplicationContext(), "To prevent memory leaks barcode scanner has been stopped", Toast.LENGTH_SHORT).show();
            }


            @Override
            public void receiveDetections(Detector.Detections<Barcode> detections) {
                final SparseArray<Barcode> barcodes = detections.getDetectedItems();
                if (barcodes.size() != 0) {


                    barcodeText.post(new Runnable() {

                        @Override
                        public void run() {

                            if (barcodes.valueAt(0).email != null) {
                                barcodeText.removeCallbacks(null);
                                barcodeData = barcodes.valueAt(0).email.address;
                                barcodeText.setText(barcodeData);
                                toneGen1.startTone(ToneGenerator.TONE_CDMA_PIP, 150);
                            } else {

                                barcodeData = barcodes.valueAt(0).displayValue;
                                barcodeText.setText(barcodeData);
                                toneGen1.startTone(ToneGenerator.TONE_CDMA_PIP, 150);

                                boolean noData = false;

                                databaseReference.addValueEventListener(new ValueEventListener() {
                                    @Override
                                    public void onDataChange(DataSnapshot dataSnapshot) {

                                        if (dataSnapshot.exists()){

                                            // this method is call to get the realtime
                                            // updates in the data.
                                            // this method is called when the data is
                                            // changed in our Firebase console.
                                            // below line is for getting the data from
                                            // snapshot of our database.

                                            for (DataSnapshot vs : dataSnapshot.getChildren()) {
                                                //String dbBarcode = ds.child("p_barcode").getValue(String.class);
                                                //Toast.makeText(MainActivity.this, "ygdyqwgdywqdgyqwgd", Toast.LENGTH_SHORT).show();

                                                if (vs.getKey().equals(barcodeData)) {
                                                    dbName = vs.child("p_name").getValue(String.class);
                                                    dbPrice = vs.child("p_price").getValue(String.class);
                                                    dbClass = vs.child("p_class").getValue(String.class);
                                                    dbAllergen = vs.child("p_allergen").getValue(String.class);
                                                    dbIngredient = vs.child("p_ingredient").getValue(String.class);

                                                    updateUI();
                                                    break;
                                                }
                                                else{
                                                    //Toast.makeText(MainActivity.this, "Product Does Not exist In Store", Toast.LENGTH_SHORT).show();

                                                    try {
                                                        Thread.sleep(2000);
                                                    } catch (InterruptedException e) {
                                                        e.printStackTrace();
                                                    }
                                                    initialiseDetectorsAndSources();
                                                }

                                            }

                                        }

                                    }

                                    @Override
                                    public void onCancelled(DatabaseError databaseError) {
                                        // calling on cancelled method when we receive
                                        // any error or we are not able to get the data.
                                        //Toast.makeText(MainActivity.this, "Fail to get data. aaaa", Toast.LENGTH_SHORT).show();
                                    }


                                });

                                //Toast.makeText(MainActivity.this, "Product Exist In Store. Fetching Data", Toast.LENGTH_SHORT).show();



                            }
                        }
                    });

                }
            }
        });


    }


    @Override
    protected void onPause() {
        super.onPause();
        getSupportActionBar().hide();
        cameraSource.release();
    }

    @Override
    protected void onResume() {
        super.onResume();
        getSupportActionBar().hide();
        initialiseDetectorsAndSources();
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

    public void updateUI(){
        //Toast.makeText(MainActivity.this, "Data Retrieved", Toast.LENGTH_SHORT).show();

        Intent intent = new Intent(MainActivity.this, ProductScan.class);

        intent.putExtra("name", dbName);
        intent.putExtra("price", dbPrice);
        intent.putExtra("class", dbClass);
        intent.putExtra("ingredient", dbIngredient);
        intent.putExtra("allergen", dbAllergen);

        startActivity(intent);
        finish();

    }

}