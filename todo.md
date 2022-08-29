- [] Send buy limit order 
- [] Wait for buy limit order to fill
- [] Send sell limit order (lo ideal es siempre vender arriba, no importa si me quedo con btc por un tiempo largo)
- [] Listen to 1m candles
- [] Keep state of last n candles 
- [] Be able to manage m of buy-sell flow in parallel
- [] Guardar a un archivo la serie de precios usando como index un timestamp para 1 hora de tiempo (cada hora copio el dataframe a otro y lo guardo en un csv)

Alternative 1:
    Sequence:
    0. While true:
        1. Listen to price every 10 seconds (request or stream) 
        2. If conditions is true then buy
        3. Wait for order to fill
        4. Get account info to get balance for BUSD
        5. Send sell order for a 0.003 ret

    Condition:
    1. If there is a consistent down of price AND price starts to go a little (0.0005) bit up for more than 30 seconds

Alternative 2:
    Same sequence but listening every 30 seconds

    Condition:
    1. If there is a consistend down of price for more than 2 minutes (save price when it starts to go down) AND grnn predict price will go up more than 0.005, then buy and automatically perform sell for a ret more than 0.005

    For trainning the pnn i only keep last hour information (120 items) I train every time i get new data

**Siempre intento compras en un rango <= -0.001% respecto del precio de venta anterior**

**Ojo porque la secuencia debería ser la reves, yo parto de tener BTC, busco vender en una subida y comprar un poco (<= -0.001%) más abajo**


Alternative 1:
    Sequence:
    0. While true:
        1. Listen to price every 15 seconds (request or stream) 
        2. If conditions is true then sell
        3. Wait for order to fill
        4. Get account info to get balance for BUSD
        5. Send Buy order for <= -0.001% ret

    Condition:
    1. If there is a consistent up of price AND price starts to go down little (0.0005) bit down for more than 30 seconds

Alternative 2:
    Same sequence but listening every 30 seconds

    Condition:
    1. If there is a consistend up of price for more than 45 seconds (save price when it starts to go up) AND grnn predict price will go down more than -0.001, then sell and automatically perform buy for a ret less than -0.001

    GRNN prediction: 
        When having price_n:

        x_train: vector of last n prices [price_0, price_1, ..., price_n-1]
        y_train: vector of last n returns [ret_0, ret_1, ..., ret_n-1]

        ret_n-1 should be calculated using price_n
        
        x_prediction: [price_n]
        y_prediction: [ret_n]

        ret_n: return predicted


    For trainning the grnn/pnn i only keep last hour information (120 items) I train every time i get new data

Que pasa si siempre compro en el avg de la ultima media hora y vendo 1.002 arriba del avg de eso?
Ejemplo:
    Media= 21350
    buyPrice = avg = 21350
    sell_price = 1.002*avg = 21392

Estaría bueno ver como variar ese "avg" y cuanto para abajo y para arriba