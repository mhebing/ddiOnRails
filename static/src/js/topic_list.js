/***
 * Topic List Design 1
 *
 * This script visualizes a tree structure of topics and their concepts, questions and variables using the fancytree library.
 * Make sure you set study and language variable in template, else api calls will not work.
 *
 * In design 1 questions and variables are integrated directly to the tree. In design 2 variables and questions will
 * be placed in another div on the right side.
 *
 * @author cstolpe
 *
 */



$.ui.fancytree.debugLevel = 0; // set debug level; 0:quiet, 1:info, 2:debug

// Define buttons, which are shown when you hover over a topic or concept
// This buttons will be append to the nodes defined by fancytree
var filter_options_string = "<span class='btn-group btn-group-sm filter-options' role='group'><button type='button' data-tooltip='tooltip' title='Show all related variables' onclick='filter(this, \"variable\")' class='btn btn-link filter-option-variable' ><span class='glyphicon glyphicon-stats' aria-hidden='true'></span></button><button type='button' class='btn btn-link filter-option-question' data-tooltip='tooltip' title='Show all related questions' onclick='filter(this, \"question\")'><span class='glyphicon glyphicon-question-sign' aria-hidden='true'></span></button>" +
    "<button type='button' data-tooltip='tooltip' title='Add all related variables to one of your baskets' onclick='addToBasket(this)' class='btn btn-link' data-toggle='modal' data-target='#topic-list-add-to-basket'><span class='glyphicon glyphicon-shopping-cart' aria-hidden='true'></span></button></span>"
var filter_options_var_quest_string = "<span class='btn-group btn-group-sm filter-options' role='group'><button type='button' data-tooltip='tooltip' title='Go to detail view' class='btn btn-link' onclick='redirect(this)'><span class='glyphicon glyphicon-circle-arrow-right' aria-hidden='true'></span></button><button type='button' data-tooltip='tooltip' title='Add variables to one of your baskets' onclick='addToBasket(this)' class='btn btn-link btn-sm' data-toggle='modal' data-target='#topic-list-add-to-basket'><span class='glyphicon glyphicon-shopping-cart' aria-hidden='true'></span></button></span>"
var base_url = location.protocol + '//' + window.location.host + "/api/topics/" + study + "/" + language

// Define what the tree structure will look like, for more information and options see https://github.com/mar10/fancytree.
// Build and append tree to #tree.
$(function () {
    $("#tree").fancytree({
        extensions: ["filter", "glyph"],
        types: {
            "topic": {icon: "glyphicon glyphicon-folder-close"},
            "concept": {icon: "glyphicon glyphicon-asterisk"},
            "variable": {icon: "glyphicon glyphicon-stats"},
            "question": {icon: "glyphicon glyphicon-question-sign"},
        },
        filter: {  // override default settings
            counter: false, // No counter badges
            mode: "hide"  // "dimm": Grayout unmatched nodes, "hide": remove unmatched nodes
        },
        icon: function (event, data) {
            return data.typeInfo.icon;
        },
        glyph: {
            // The preset defines defaults for all supported icon types.
            // It also defines a common class name that is prepended (in this case 'fa ')
            preset: "bootstrap3",
            map: {
                _addClass: "glyphicon",
                checkbox: "glyphicon-unchecked",
                checkboxSelected: "glyphicon-check",
                checkboxUnknown: "glyphicon-expand",  // "glyphicon-share",
                dragHelper: "glyphicon-play",
                dropMarker: "glyphicon-arrow-right",
                error: "glyphicon-warning-sign",
                expanderClosed: "glyphicon-menu-right",  // glyphicon-plus-sign
                expanderLazy: "glyphicon-menu-right",  // glyphicon-plus-sign
                expanderOpen: "glyphicon-menu-down",  // glyphicon-minus-sign
                loading: "glyphicon-refresh fancytree-helper-spin",
                nodata: "glyphicon-info-sign",
                noExpander: "",
                radio: "glyphicon-remove-circle",  // "glyphicon-unchecked",
                radioSelected: "glyphicon-ok-circle",  // "glyphicon-check",
                // Default node icons.
                // (Use tree.options.icon callback to define custom icons based on node data)
                doc: "glyphicon-file",
                docOpen: "glyphicon-file",
                folder: "glyphicon-folder-close",
                folderOpen: "glyphicon-folder-open"
            }

        },
        source: {
            url: base_url,
            cache: false
        },
        renderNode: function (event, data) {
            var node = data.node;
            var d = node.data.description || '';
            var $spanTitle = $(node.span).find('span.fancytree-title');
            if ($(node.span).find('span.filter-options').length == 0) {
                if (node.type == 'topic' || node.type == 'concept') {
                    $spanTitle.after(filter_options_string);
                }
                else if (node.type == 'variable' || node.type == 'question') {
                    $spanTitle.after(filter_options_var_quest_string);
                }
            }

        },
        // When tree fully loaded: if parameter 'open' is set in URL open specified node
        init: function(event, data){
            if(open != null) {
                var node = $("#tree").fancytree("getNodeByKey", open);
                node.makeVisible();
            }
        }
    });

    // Search the tree for search string
    $('#btn-search').on('click', function () {
        $("#tree").fancytree("getTree").filterBranches($('#search').val(), {autoExpand: true});
    });

    // Trigger search on enter
    $('.search-bar').keypress(function(e){
        if(e.which == 13){//Enter key pressed
            $('#btn-search').click();
        }
    });

    // Activate tooltip for more information about filter buttons, e.g. 'Show all related variables'
    $('body').tooltip({selector:'[data-tooltip=tooltip]', trigger: "hover"});

});

// On click on a topic or concept show all variables oder questions
// Pay attention to the different states of the tree (has children / has no children / children already shown)
function filter(node, type) {

    var activeNode = $.ui.fancytree.getNode(node);

    var extraClasses = activeNode.extraClasses || "";
    var url = base_url + "/" + activeNode.key;
    if(type == 'variable'){
        url += '?variable_html=true';
    } if(type == 'question'){
        url += '?question_html=true';
    }
    var data;
    jQuery.getJSON(url, function (json) {
        data = json;
        if (activeNode.hasChildren() && !$(activeNode.li).hasClass(type + '-btn-active')) {
            removeAllChildren(activeNode, type);
            if (type == 'variable') {
                for (var i = 0; i < data.variable_list.length; i++) {
                    var concept_key = data.variable_list[i].concept_key.toString();
                    data.variable_list[i]['extraClasses'] = 'async-data-' + type;
                    var parentNode = $("#tree").fancytree("getNodeByKey", concept_key);
                    parentNode.addChildren(data.variable_list[i]);
                    // $(parentNode).addClass(type + '-btn-active')
                }
            }
            if (type == 'question') {
                if (data.question_list) {
                    for (var i = 0; i < data.question_list.length; i++) {
                        var concept_key = data.question_list[i].concept_key.toString();
                        data.question_list[i]['extraClasses'] = 'async-data-' + type;
                        var parentNode = $("#tree").fancytree("getNodeByKey", concept_key);
                        parentNode.addChildren(data.question_list[i]);
                    }
                }
            }
            $(activeNode.li).addClass(type + '-btn-active')
            activeNode.visit(function (node) {
                node.removeClass('fancytree-hide')
                node.setExpanded(true);
                $(node.li).addClass(type + '-btn-active')
            }, true);

            activeNode.setExpanded(true);
        }
        else if (activeNode.hasChildren() && $(activeNode.li).hasClass(type + '-btn-active')) {
            removeAllChildren(activeNode, type);
            $(activeNode.li).removeClass(type + '-btn-active')
            activeNode.visit(function (node) {
                if (node.type == 'topic' || node.type == 'concept') {
                    $(node.li).removeClass(type + '-btn-active')
                }
            }, true);
        }
        else if (!activeNode.hasChildren() && !$(activeNode.li).hasClass(type + '-btn-active')) {
            if (type == 'variable') {
                for (var i = 0; i < data.variable_list.length; i++) {
                    var concept_key = data.variable_list[i].concept_key.toString();
                    data.variable_list[i]['extraClasses'] = 'async-data-' + type;
                    var parentNode = $("#tree").fancytree("getNodeByKey", concept_key);
                    parentNode.addChildren(data.variable_list[i]);
                    $(parentNode.li).addClass(type + '-btn-active')
                    parentNode.setExpanded(true)
                }
            }
            if (type == 'question') {
                if (data.question_list) {
                    for (var i = 0; i < data.question_list.length; i++) {
                        var concept_key = data.question_list[i].concept_key.toString();
                        data.question_list[i]['extraClasses'] = 'async-data-' + type;
                        var parentNode = $("#tree").fancytree("getNodeByKey", concept_key);
                        parentNode.addChildren(data.question_list[i]);
                        parentNode.setExpanded(true)
                    }
                }
            }
            $(activeNode).toggleClass(type + '-btn-active')
            activeNode.visit(function (node) {
                node.removeClass('fancytree-hide')
                node.setExpanded(true);
                $(node.li).addClass(type + '-btn-active')
            }, true);

            activeNode.setExpanded(true);
        }
        else if (!activeNode.hasChildren() && $(activeNode).hasClass(type + '-btn-active')) {
            removeAllChildren(activeNode, type);
            $(activeNode).removeClass(type + '-btn-active')
        }

    });
}

function toggleChildren(node) {
    var node = $.ui.fancytree.getNode(node);
    var children = node.getChildren();

    if (children) {
        for (var i = 0; i < children.length; i++) {
//                    children[i].toggleClass('hide');
        }
    }
}


// Remove all variables and questions from active node
function removeAsyncLoadedData(activeNode, type) {
    var children = activeNode.getChildren();
    var tmp = [];
    if (children) {
        for (var i = 0; i < children.length; i++) {
            var node = $.ui.fancytree.getNode(children[i]);
            var extraClasses = node.extraClasses || "";
            if (extraClasses.includes('async-data-' + type)) {
                tmp.push(node);
            }
        }
        for (var i = 0; i < tmp.length; i++) {
            tmp[i].remove();
        }
    }
}

// Remove all child nodes from active node
function removeAllChildren(activeNode, type) {
    var tmp = [];
    activeNode.visit(function (node) {
        if (node.type == type) {
            tmp.push(node);
        }
    }, true)

    for (var i = 0; i < tmp.length; i++) {
        tmp[i].remove();
    }
}

// Show more information for adding an elment to the basket (how many variables will be added to the basket) and render
// a list of the user's baskets
function addToBasket(el) {
    var node = $.ui.fancytree.getNode(el);
    var url = base_url + "/" + node.key + "?variable_list=false";
    $('#basket_list').empty();
    var number_of_variables = '?';
    if (node.type == 'variable') {
        number_of_variables = 1;
        $('#number_of_variables').text(number_of_variables); // Set number of variables in add to basket modal

    } else {
        jQuery.getJSON(url, function (data) {
            number_of_variables = data.variable_count || '?';
            $('#number_of_variables').text(number_of_variables); // Set number of variables in add to basket modal
        })
    }

    var url = base_url + "/baskets";
    jQuery.getJSON(url, function (data) {
        if(data.user_logged_in) {
            if(data.baskets.length == 0){
                var redirect_create_basket_url = location.protocol + '//' + window.location.host + "/workspace/baskets";
                $('#basket_list').append("<p><a class='btn btn-primary' href='" + redirect_create_basket_url + "'>Create a basket</a></p>");
            }
            for (var i = 0; i < data.baskets.length; i++) {
                var addToBasketFunction = "addToBasketRequest(\'" + node.key + "\'," + data.baskets[i].id + ")"
                $('#basket_list').append("<p><button class='btn btn-primary' onclick=" + addToBasketFunction + ">Add to basket <strong>" + data.baskets[i].name + "</strong></button></p>");
            }
        } else {
            var redirect_login_url = location.protocol + '//' + window.location.host + "/workspace/login";
            $('#basket_list').append("<p><a class='btn btn-primary' href='" + redirect_login_url + "'>Please log in to use this function.</a></p>");
        }
    });
}

// Call API to add an element (identified by node_key) to a basket (identified by basket_id)
// On success show success message else error message
function addToBasketRequest(node_key, basket_id) {
    var url = base_url + "/" + node_key + "/add_to_basket/" + basket_id;
    jQuery.get(url, function (data) {
    }).done(function () {
        $('#basket_success').removeClass('hidden');
    }).fail(function () {
        $('#basket_error').removeClass('hidden');
    })
}

// Remove status alerts from modal after modal was closed
$('#topic-list-add-to-basket').on('hidden.bs.modal', function () {
    $('#basket_success').addClass('hidden');
    $('#basket_error').addClass('hidden');
})


// redirect to detail page of element
function redirect(el) {
    var node = $.ui.fancytree.getNode(el);
    var url = location.protocol + '//' + window.location.host + "/api/topics/redirect/" + node.key;
    window.location.href = url;
}

