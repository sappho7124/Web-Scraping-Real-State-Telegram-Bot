/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package real_state.kumi;

/**
 *
 * @author santi
 */
import org.telegram.telegrambots.bots.TelegramLongPollingBot;
import org.telegram.telegrambots.meta.api.methods.send.SendMessage;
import org.telegram.telegrambots.meta.api.objects.Message;
import org.telegram.telegrambots.meta.api.objects.Update;
import org.telegram.telegrambots.meta.exceptions.TelegramApiException;
import java.util.regex.Matcher;
import java.util.regex.Pattern;


public class Bot extends TelegramLongPollingBot {

    @Override
public void onUpdateReceived(Update update) {
    // We check if the update has a message and the message has text
    if (update.hasMessage() && update.getMessage().hasText()) {
        String message_text = update.getMessage().getText();
        if(message_text.equals("/kill")){
            SendMessage message = new SendMessage(); // Create a SendMessage object with mandatory fields
            message.setChatId(update.getMessage().getChatId().toString());
            message.setText("Killing Bot, it must be manually turned on later");
            try {
                execute(message); // Call method to send the message
                System.exit(0);
            } catch (TelegramApiException e) {
                e.printStackTrace();
            }
        }
        if(message_text.contains("/test")){
            SendMessage message = new SendMessage(); // Create a SendMessage object with mandatory fields
            message.setChatId(update.getMessage().getChatId().toString());
            message.setText("Bot Funciona pipipipipipi");
            try {
                execute(message); // Call method to send the message
            } catch (TelegramApiException e) {
                e.printStackTrace();
            }
        }
        if(message_text.contains("/find")){
            SendMessage message = new SendMessage(); // Create a SendMessage object with mandatory fields
            message.setChatId(update.getMessage().getChatId().toString());
            String input = message_text;
            String patternString = "/find\\s+(\\w+)\\s+(\\d+)-(\\d+)";
            // Compile the pattern
            Pattern pattern = Pattern.compile(patternString);

            // Match the pattern against the input string
            Matcher matcher = pattern.matcher(input);

            // Check if a match is found
            if (matcher.matches()) {
                // Extract the province name, min value, and max value
                String province = matcher.group(1);
                int minValue = Integer.parseInt(matcher.group(2));
                int maxValue = Integer.parseInt(matcher.group(3));

                // Print the extracted values
                System.out.println("Province: " + province);
                System.out.println("Min Value: " + minValue);
                System.out.println("Max Value: " + maxValue);
                message.setText("Los valores que ingresaste fueron: Provincia: " + province + " / Min: " + minValue+" / Max: "+maxValue);
            } else {
                System.out.println("No te entendi, escribe el mensaje siguiendo este formato: /find [provincia] [valor minimo]-[valor maximo]");
            }
            try {
                execute(message); // Call method to send the message
            } catch (TelegramApiException e) {
                e.printStackTrace();
            }
        }
    }
}

    @Override
    public String getBotUsername() {
        return "KUMI";
    }

    @Override
    public String getBotToken() {
        return "6100423014:AAH9MhBBKAfPEfsYd08yaDLZS4MANHyg-tA";
    }

    
}
