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

# Models

@EventPrice = (data) ->
    @id = ko.observable(if data then data.event_id else 0)
    @buy_for_price = ko.observable(if data then data.buy_for_price else 0)
    @buy_against_price = ko.observable(if data then data.buy_against_price else 0)
    @sell_for_price = ko.observable(if data then data.sell_for_price else 0)
    @sell_against_price = ko.observable(if data then data.sell_against_price else 0)

    @update = (data) =>
        @id(data.event_id)
        @buy_for_price(data.buy_for_price)
        @buy_against_price(data.buy_against_price)
        @sell_for_price(data.sell_for_price)
        @sell_against_price(data.sell_against_price)
        return

    return

@UserStatistics = (data) -> 
    @id = ko.observable(if data then data.user_id else 0)
    @total_cash = ko.observable(if data then data.total_cash else 0)

    @update = (data) =>
        @id(data.user_id)
        @total_cash(data.total_cash)
        return

    return

@Bet = (outcome) -> 
    @outcome = outcome
    @bought_avg_price = ko.observable(0)
    @sold_avg_price = ko.observable(0)
    @has = ko.observable(0)

    @update = (data) =>
        @bought_avg_price(data.bought_avg_price)
        @sold_avg_price(data.sold_avg_price)
        @has(data.has)
        return

    return

@BetsVM = ->
    @for = new Bet(true)
    @against = new Bet(false)

    @update = (data) =>
        @for.update data.for
        @against.update data.against
        return

    return
