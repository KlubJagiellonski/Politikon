ko.bindingHandlers.flashText =
    init: (element, valueAccessor, allBindingsAccessor, viewModel, bindingContext) ->
        val = "" + ko.utils.unwrapObservable(valueAccessor())
        $(element).text val
    update: (element, valueAccessor, allBindingsAccessor, viewModel, bindingContext) ->
        $el = $(element)
        val = "" + ko.utils.unwrapObservable(valueAccessor())

        return if ($el.text() == val)

        $el.text val
        # animate
        $el.stop true, false
        $el.animate 'font-size': "1.6em", 300, () -> $(this).animate('font-size': "1.2em", 300)

ko.bindingHandlers.bootstrapButtonLoading =
    init: (element, valueAccessor, allBindingsAccessor, viewModel, bindingContext) ->
        $el = $(element)
    update: (element, valueAccessor, allBindingsAccessor, viewModel, bindingContext) ->
        $el = $(element)
        val = ko.utils.unwrapObservable(valueAccessor())

        if val
            $el.button('loading')
        else
            $el.button('reset')

# Models

@Event = (data, betsVM) ->
    @id = ko.observable(if data then data.event_id else 0)
    @buy_for_price = ko.observable(if data then data.buy_for_price else 0)
    @buy_against_price = ko.observable(if data then data.buy_against_price else 0)
    @sell_for_price = ko.observable(if data then data.sell_for_price else 0)
    @sell_against_price = ko.observable(if data then data.sell_against_price else 0)

    @loading_buy_YES = ko.observable(false)
    @loading_buy_NO = ko.observable(false)
    @loading_sell_YES = ko.observable(false)
    @loading_sell_NO = ko.observable(false)

    @bets = ko.observableArray([])
    @betsVM = betsVM

    @bet_for_YES = ko.computed 
        read: =>
            @betsVM.bet_for_event_and_outcome @, 'YES'
    @bet_for_NO = ko.computed 
        read: =>
            @betsVM.bet_for_event_and_outcome @, 'NO'

    @has_bets_for_YES = ko.computed 
        read: =>
            bet = @bet_for_YES()

            return 0 if (bet == null)
            return bet.has()

    @has_bets_for_NO = ko.computed 
        read: =>
            bet = @bet_for_NO()

            return 0 if (bet == null)
            return bet.has()

    @buy_YES = =>
        @loading_buy_YES(true)
        @createTransaction true, 'YES', @buy_for_price(), => @loading_buy_YES(false)
    @buy_NO = =>
        @loading_buy_NO(true)
        @createTransaction true, 'NO', @buy_against_price(), => @loading_buy_NO(false)
    @sell_YES = =>
        @loading_sell_YES(true)
        @createTransaction false, 'YES', @buy_for_price(), => @loading_sell_YES(false)
    @sell_NO = =>
        @loading_sell_NO(true)
        @createTransaction false, 'NO', @buy_against_price(), => @loading_sell_NO(false)

    @createTransactionUrl = =>
        "/events/event/#{@id()}/transaction/create/"

    @createTransaction = (buy=true, outcome='YES', for_price=0.0, callback= => return) =>
        console.log buy, outcome, for_price

        payload = 
            buy: buy
            outcome: outcome
            for_price: for_price

        $.ajax 
            url: @createTransactionUrl(),
            type: 'POST',
            data:  payload,
            dataType: 'json',
            timeout: 20000,
            tryCount: 0,
            retryLimit: 3,
            success: (json) ->
                console.log(json)
                callback()
            error: (xhr, textStatus, errorThrown) ->
                console.log xhr, textStatus, errorThrown

                if (textStatus == 'timeout')
                    @tryCount++
                    if (@tryCount <= @retryLimit)
                        $.ajax(@)
                        return

                    errorCallback()
                    return
                
                if (xhr.status == 500)
                    alert('Oops! There seems to be a server problem, ase try again later.');
                else
                    alert('Oops! There was a problem, sorry.');

                callback()

    @update = (data) =>
        @id(data.event_id)
        @buy_for_price(data.buy_for_price)
        @buy_against_price(data.buy_against_price)
        @sell_for_price(data.sell_for_price)
        @sell_against_price(data.sell_against_price)
        return

    return

@EventsVM = (data, betsVM) ->
    @betsVM = betsVM

    @events = ko.observableArray([])

    @firstEvent = =>
        return null if @events().length == 0

        return @events()[0]

    @update = (data) =>
        for dataItem in data
            event = ko.utils.arrayFirst @events(), (item) -> dataItem.event_id == item.id
            if event == null
                event = new Event(dataItem, @betsVM)
                @events.push event
            else
                event.update(dataItem)

        return

    @update(data) if data
    return


@UserStatistics = (data) -> 
    @id = ko.observable(if data then data.user_id else 0)
    @total_cash = ko.observable(if data then data.total_cash else 0)

    @update = (data) =>
        @id(data.user_id)
        @total_cash(data.total_cash)
        return

    return

@Bet = (data) -> 
    @id = ko.observable(if data then data.bet_id else 0)
    @event_id = ko.observable(if data then data.event_id else 0)
    @user_id = ko.observable(if data then data.user_id else 0)
    @outcome = ko.observable(if data then data.outcome else 0)
    @has = ko.observable(if data then data.has else 0)
    @bought = ko.observable(if data then data.bought else 0)
    @sold = ko.observable(if data then data.sold else 0)
    @bought_avg_price = ko.observable(if data then data.bought_avg_price else 0)
    @sold_avg_price = ko.observable(if data then data.sold_avg_price else 0)
    @rewarded_total = ko.observable(if data then data.rewarded_total else 0)

    @update = (data) =>
        @id(data.bet_id)
        @event_id(data.event_id)
        @user_id(data.user_id)
        @outcome(data.outcome)
        @has(data.has)
        @bought(data.bought)
        @sold(data.sold)
        @bought_avg_price(data.bought_avg_price)
        @sold_avg_price(data.sold_avg_price)
        @rewarded_total(data.rewarded_total)

        return

    return

@BetsVM = (data) ->
    @bets = ko.observableArray([])

    @bet_for_event_and_outcome = (event, outcome) =>
        bets_for_event = ko.utils.arrayFilter @bets(), (item) -> item.event_id() == event.id()
        bet = ko.utils.arrayFirst bets_for_event, (item) -> item.outcome() == outcome

        return bet

    @update = (data) =>
        for dataItem in data
            bet = ko.utils.arrayFirst @bets(), (item) -> dataItem.bet_id == item.id
            if bet == null
                @bets.push new Bet(dataItem)
            else
                bet.update(dadataItemta)

        return

    @update(data) if data
    return

@AppDataStore = (data) ->
    @message = ko.observable("")

    @userVM = new UserStatistics(data['user'] if data)
    @betsVM = new BetsVM(data['bets'] if data)
    @eventsVM = new EventsVM(data['events'] if data, @betsVM)

    return