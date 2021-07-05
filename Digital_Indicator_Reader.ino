#define DataPin A0
#define ClkPin  A1

// UART speed
#define UARTBaudRate 115200

// ADC threshold, ADC values greater than this are interpreted as logical 1, see loop()
#define ADC_Threshold 140

// data format
#define DATA_BITS_LEN 24
#define INCH_BIT 23
#define SIGN_BIT 20
#define START_BIT -1 // -1 - no start bit

// data capture and decode functions
bool getRawBit() {
    bool data;
    while (analogRead(ClkPin) > ADC_Threshold)
        ;
    while (analogRead(ClkPin) < ADC_Threshold)
        ;
    data = analogRead(DataPin) > ADC_Threshold;
    return data;
}

long getRawData() {
    long out = 0;
    for (int i = 0; i < DATA_BITS_LEN; i++) {
        out |= getRawBit() ? 1L << DATA_BITS_LEN : 0L;
        out >>= 1;
    }
    return out;
}

long getValue(bool &inch) {
    long out = getRawData();
    inch = out & (1L << INCH_BIT);
    bool sign = out & (1L << SIGN_BIT);
    out &= (1L << SIGN_BIT) - 1L;
    out >>= (START_BIT+1);
    if (sign)
        out = -out;
    return out;
}

// Arduino setup and main loop

// defines for setting and clearing register bits
#ifndef cbi
#define cbi(sfr, bit) (_SFR_BYTE(sfr) &= ~_BV(bit))
#endif
#ifndef sbi
#define sbi(sfr, bit) (_SFR_BYTE(sfr) |= _BV(bit))
#endif

void setup() {
    // set ADC prescale to 16 (set ADC clock to 1MHz)
    // this gives as a sampling rate of ~77kSps
    sbi(ADCSRA, ADPS2);
    cbi(ADCSRA, ADPS1);
    cbi(ADCSRA, ADPS0);

    Serial.begin(UARTBaudRate);
}

void loop() {
    bool inch;
    long value;

    value = getValue(inch);
    Serial.print(value);
    if(inch) Serial.print(",1");
    else Serial.print(",0");
    Serial.println();
}

