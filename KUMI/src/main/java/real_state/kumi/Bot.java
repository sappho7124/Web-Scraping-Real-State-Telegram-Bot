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
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;



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
        if(message_text.contains("/datatest")){
            SendMessage message = new SendMessage(); // Create a SendMessage object with mandatory fields
            message.setChatId(update.getMessage().getChatId().toString());
            message.setText("Mirar logs");
            try {
                String url = "jdbc:sqlite:realestate_data_spain.db";
        
                try (Connection connection = DriverManager.getConnection(url);
                     Statement statement = connection.createStatement()) {

                    String query = "SELECT * FROM realestate_data";
                    ResultSet resultSet = statement.executeQuery(query);

                    while (resultSet.next()) {
                        // Retrieve data from the result set
                        String price = resultSet.getString("price");
                        String size = resultSet.getString("size");
                        String province = resultSet.getString("province");
                        // ... retrieve other columns

                        // Process the retrieved data as needed
                        System.out.println("Price: " + price);
                        System.out.println("Size: " + size);
                        System.out.println("province: " + province);
                        // ... print or use other columns as required
                    }

                } catch (SQLException e) {
                    e.printStackTrace();
                }
                execute(message); // Call method to send the message
            } catch (TelegramApiException e) {
                e.printStackTrace();
            }
        }
        if(message_text.contains("/help")){
            SendMessage message = new SendMessage(); // Create a SendMessage object with mandatory fields
            message.setChatId(update.getMessage().getChatId().toString());
            try {
                message.setText("Comandos disponibles:\n/help lista de comandos disponibles\n/findprice encuentra propiedades en un rango de precios en una provincia\n/findsize encuentra propiedades en un rango de metraje en una provincia\nPara usar un comando de find usa este formato: /find... [tamaño] [valor minimo]-[valor maximo]");
                execute(message); // Call method to send the message
            } catch (TelegramApiException e) {
                e.printStackTrace();
            }
        }
        if(message_text.contains("/start")){
            SendMessage message = new SendMessage(); // Create a SendMessage object with mandatory fields
            message.setChatId(update.getMessage().getChatId().toString());
            try {
                message.setText("Bot para encontrar propiedades en españa, Creado por: \nSantiago Mejia\nDaniel Bautista\nKevin Llanos\nCristian Muñoz");
                execute(message); // Call method to send the message
            } catch (TelegramApiException e) {
                e.printStackTrace();
            }
        }
        if(message_text.contains("/findprice")){
            /**SendMessage message = new SendMessage(); // Create a SendMessage object with mandatory fields
            message.setChatId(update.getMessage().getChatId().toString());*/
            String input = message_text;
            String patternString = "/findprice\\s+(\\w+)\\s+(\\d+)-(\\d+)";
            // Compile the pattern
            Pattern pattern = Pattern.compile(patternString);

            // Match the pattern against the input string
            Matcher matcher = pattern.matcher(input);

            // Check if a match is found
            if (matcher.matches()) {
                SendMessage message = new SendMessage(); // Create a SendMessage object with mandatory fields
                message.setChatId(update.getMessage().getChatId().toString());
                // Extract the province name, min value, and max value
                String province_given = matcher.group(1);
                int minValue = Integer.parseInt(matcher.group(2));
                int maxValue = Integer.parseInt(matcher.group(3));

                // Print the extracted values
                System.out.println("Province: " + province_given);
                System.out.println("Min Value: " + minValue);
                System.out.println("Max Value: " + maxValue);
                message.setText("Los valores que ingresaste fueron: Provincia: " + province_given + " / Min: " + minValue+" / Max: "+maxValue);
                try {
                    execute(message); // Call method to send the message
                } catch (TelegramApiException e) {
                    e.printStackTrace();
                }
                        
                try (Connection conn = DriverManager.getConnection("jdbc:sqlite:realestate_data_spain.db");
                Statement stmt = conn.createStatement();
                ResultSet rs = stmt.executeQuery("SELECT * FROM realestate_data WHERE province = '" + province_given + "' AND price >= " + minValue + " AND price <= " + maxValue)) {
                System.out.println("rs: " + rs);
                    while (rs.next()) {
                        
                        
                        String price = rs.getString("price");
                        String size = rs.getString("size");
                        String location = rs.getString("location");
                        String province = rs.getString("province");
                        String title = rs.getString("title");
                        String url = rs.getString("url");
                        
                        /**System.out.println("price: " + price);
                        System.out.println("size: " + size);
                        System.out.println("location: " + location);
                        System.out.println("province: " + province);
                        System.out.println("title: " + title);
                        System.out.println("url: " + url);*/
                        
                        
                        message.setText("Precio: "+price+"\nMetraje: "+size+" m\nTitulo: "+title+"\nUbicacion: "+location+"\nUrl: "+url);
                        try {
                            execute(message); // Call method to send the message
                        } catch (TelegramApiException e) {
                            e.printStackTrace();
                        }
                        
                        
                        /**RealEstateData data = new RealEstateData(price, size, location, province, title, url);
                        dataList.add(data);*/
                    }
                } catch (SQLException e) {
                    System.out.println("Error retrieving data from the database: " + e.getMessage());
                }
                
            } else {
                SendMessage message = new SendMessage();
                message.setChatId(update.getMessage().getChatId().toString());
                message.setText("No te entendi, escribe el mensaje siguiendo este formato: /findprice [provincia] [valor minimo]-[valor maximo]");
                System.out.println("No te entendi, escribe el mensaje siguiendo este formato: /findprice [provincia] [valor minimo]-[valor maximo]");
            }
            /**
            try {
                execute(message); // Call method to send the message
            } catch (TelegramApiException e) {
                e.printStackTrace();
            }*/
        }
        if(message_text.contains("/findsize")){
            /**SendMessage message = new SendMessage(); // Create a SendMessage object with mandatory fields
            message.setChatId(update.getMessage().getChatId().toString());*/
            String input = message_text;
            String patternString = "/findsize\\s+(\\w+)\\s+(\\d+)-(\\d+)";
            // Compile the pattern
            Pattern pattern = Pattern.compile(patternString);

            // Match the pattern against the input string
            Matcher matcher = pattern.matcher(input);

            // Check if a match is found
            if (matcher.matches()) {
                SendMessage message = new SendMessage(); // Create a SendMessage object with mandatory fields
                message.setChatId(update.getMessage().getChatId().toString());
                // Extract the province name, min value, and max value
                String province_given = matcher.group(1);
                int minValue = Integer.parseInt(matcher.group(2));
                int maxValue = Integer.parseInt(matcher.group(3));

                // Print the extracted values
                System.out.println("Province: " + province_given);
                System.out.println("Min Value: " + minValue);
                System.out.println("Max Value: " + maxValue);
                message.setText("Los valores que ingresaste fueron: Provincia: " + province_given + " / Min: " + minValue+" / Max: "+maxValue);
                try {
                    execute(message); // Call method to send the message
                } catch (TelegramApiException e) {
                    e.printStackTrace();
                }
                        
                try (Connection conn = DriverManager.getConnection("jdbc:sqlite:realestate_data_spain.db");
                Statement stmt = conn.createStatement();
                ResultSet rs = stmt.executeQuery("SELECT * FROM realestate_data WHERE province = '" + province_given + "' AND size >= " + minValue + " AND size <= " + maxValue)) {
                System.out.println("rs: " + rs);
                    while (rs.next()) {
                        
                        
                        String price = rs.getString("price");
                        String size = rs.getString("size");
                        String location = rs.getString("location");
                        String province = rs.getString("province");
                        String title = rs.getString("title");
                        String url = rs.getString("url");
                        
                        /**System.out.println("price: " + price);
                        System.out.println("size: " + size);
                        System.out.println("location: " + location);
                        System.out.println("province: " + province);
                        System.out.println("title: " + title);
                        System.out.println("url: " + url);*/
                        
                        
                        message.setText("Precio: "+price+"\nMetraje: "+size+" m\nTitulo: "+title+"\nUbicacion: "+location+"\nUrl: "+url);
                        try {
                            execute(message); // Call method to send the message
                        } catch (TelegramApiException e) {
                            e.printStackTrace();
                        }
                        
                        
                        /**RealEstateData data = new RealEstateData(price, size, location, province, title, url);
                        dataList.add(data);*/
                    }
                } catch (SQLException e) {
                    System.out.println("Error retrieving data from the database: " + e.getMessage());
                }
                
            } else {
                SendMessage message = new SendMessage();
                message.setChatId(update.getMessage().getChatId().toString());
                message.setText("No te entendi, escribe el mensaje siguiendo este formato: /findsize [provincia] [valor minimo]-[valor maximo]");
                System.out.println("No te entendi, escribe el mensaje siguiendo este formato: /findsize [provincia] [valor minimo]-[valor maximo]");
            }
            /**
            try {
                execute(message); // Call method to send the message
            } catch (TelegramApiException e) {
                e.printStackTrace();
            }*/
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
