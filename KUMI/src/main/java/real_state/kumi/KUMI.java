/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 */

package real_state.kumi;

import org.telegram.telegrambots.meta.TelegramBotsApi;
import org.telegram.telegrambots.meta.exceptions.TelegramApiException;
import org.telegram.telegrambots.updatesreceivers.DefaultBotSession;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.Statement;
import java.sql.SQLException;
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

/**
 *
 * @author santi
 */
public class KUMI {
    private static void importCsvData(Connection connection, String csvFile) throws SQLException {
        String tableName = "realestate_data";
        String csvDelimiter = ",";
        String sqlCreateTable = "CREATE TABLE IF NOT EXISTS " + tableName + " (price INTEGER, size INTEGER, location TEXT, province TEXT, title TEXT, url TEXT)";
        String sqlInsert = "INSERT INTO " + tableName + " (price, size, location, province, title, url) VALUES (?, ?, ?, ?, ?, ?)";

        try (Statement statement = connection.createStatement();
            BufferedReader reader = new BufferedReader(new FileReader(csvFile))) {
            // Create the table if it doesn't exist
            statement.executeUpdate(sqlCreateTable);

            // Read the CSV file and insert the data into the table
            String line;
            while ((line = reader.readLine()) != null) {
                String[] data = line.split(csvDelimiter);

                // Insert the data into the table
                try (java.sql.PreparedStatement preparedStatement = connection.prepareStatement(sqlInsert)) {
                    for (int i = 0; i < data.length; i++) {
                        preparedStatement.setString(i + 1, data[i]);
                    }
                    preparedStatement.executeUpdate();
                }
            }
            System.out.println("CSV data imported into the database successfully.");
        } catch (IOException e) {
            System.out.println("Error reading the CSV file: " + e.getMessage());
        }
    }
    public static void main(String[] args) {
        try {
            TelegramBotsApi botsApi = new TelegramBotsApi(DefaultBotSession.class);
            botsApi.registerBot(new Bot());
        } catch (TelegramApiException e) {
            e.printStackTrace();
        }
        String databaseFile = "realestate_data_spain.db";
        String connectionString = "jdbc:sqlite:" + databaseFile;

        try (Connection connection = DriverManager.getConnection(connectionString)) {
            // Call a method to import CSV data into the database
            importCsvData(connection, "src/main/java/real_state/kumi/realestate_data_spain.csv");
            System.out.println("Connected to the database successfully.");
        } catch (SQLException e) {
            System.out.println("Error connecting to the database: " + e.getMessage());
        }
    }
}

    

