/***
 * jQuery qTips
 *
 * qTips is a jQuery plugin that allows you to quickly and easily add simple tooltips 
 * to any element or group of elements by using standard jQuery selectors.
 *
 * @name jquery.qtips.js
 * @author Daniel Wilhelm II Murdoch (wilhelm.murdoch@gmail.com)
 * @version 1.0.0 Alpha
 * @date February 19, 2009
 * @category jQuery plugin
 * @copyright (c) 2009 Daniel Wilhelm II Murdoch (wilhelm.murdoch@gmail.com)
 * @license CC Attribution 2.5 Australia - http://creativecommons.org/licenses/by/2.5/au/
 * @example Visit http://www.thedrunkenepic.com/dev/jquery/qtips/
 ***/
(function($)
{
	$.fn.qtip = function(options)
	{
		var defaults =
		{
			container: 'qtip',
			content: '',
			position: 'center',
			nudge_top: 10,
			nudge_left: 0,
			preRender: function(e, tip){},
			postRender: function(e, tip){},
			onShow: function(e, tip){},
			onHide: function(e, tip){}
		};

		var options = $.extend(defaults, options);

		return this.each(function(i)
		{
			options.preRender($(this), $('#' + options.container + i));

			$('<div></div>').prependTo('body')
							.append($('<div></div>').append(options.content))
							.addClass('qtip-wrapper')
							.attr('id', options.container + i);

			$(this).hover(function()
			{
				var height = $('#' + options.container + i).height();
				var width = $('#' + options.container + i).width();

				switch(options.position)
				{
					default:
					case 'center':

						var top  = $(this).offset().top - (height + options.nudge_top);
						var left = $(this).offset().left + ($(this).width() / 2) + options.nudge_left - (width / 2);

						break;

					case 'left':

						var top  = $(this).offset().top - (height + options.nudge_top);
						var left = $(this).offset().left + options.nudge_left;

						break;

					case 'right':

						var top  = $(this).offset().top - (height + options.nudge_top);
						var left = $(this).offset().left + $(this).width() + options.nudge_left;

						break;

					case 'bottom':

						var top  = $(this).offset().top + ($(this).height() + options.nudge_top);
						var left = $(this).offset().left + ($(this).width() / 2) + options.nudge_left - (width / 2);

						break;
				}

				$('#' + options.container + i).fadeIn('fast').css('left', left).css('top', top);

				options.onShow($(this), $('#' + options.container + i));
			},
			function()
			{
				$('#' + options.container + i).fadeOut('fast');

				options.onHide($(this), $('#' + options.container + i));
			});

			options.postRender($(this), $('#' + options.container + i));
		});
	};
})(jQuery);