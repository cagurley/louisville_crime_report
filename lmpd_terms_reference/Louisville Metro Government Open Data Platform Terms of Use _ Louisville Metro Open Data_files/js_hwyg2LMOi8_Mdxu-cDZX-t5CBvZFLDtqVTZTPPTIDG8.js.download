(function($) {
  Drupal.behaviors.panopolyImagesModule = {
    attach: function (context, settings) {
      var captions = $('.caption', context).has('img');
      $(captions).once('panopoly-images').imagesLoaded(function () {
        panopolyImagesResizeCaptionBox(captions);
      });

      function panopolyImagesResizeCaptionBox(captions) {
        captions.each(function() {
          var imageSet = $('img', this),
              imgBoxWidth = getImgWidth(imageSet),
              wrapperBoxWidth =
                  getWrapperSpacing($('.caption-inner', this))
                + getWrapperSpacing($('.caption-width-container', this)),
              totalWidth = imgBoxWidth + wrapperBoxWidth;
          $(this).width(totalWidth);
        });
      }

      // Get width of image plus margins, borders and padding
      function getImgWidth(imageSet) {
        var imgWidth = 0,
            imgBoxExtra = 0,
            testWidth = 0;
        var attrWidth;

        // We shouldn't have more than one image in a caption, but it would be
        // possible, so we make sure we have the widest one
        for (var i = 0; i < imageSet.length; i++) {
          // If we have a hardcoded width attribute from manual resizing in
          // TinMCE, use that. If not, use the image naturalWidth. We can't
          // reliably use width() for responsive images.
          attrWidth = $(imageSet[i]).attr("width");
          if (typeof attrWidth !== 'undefined') {
            // attr() returns a string. Must convert to int for math to work.
            testWidth = parseInt(attrWidth, 10);
          }
          else {
            testWidth = imageSet[i].naturalWidth;
          }
          if (testWidth > imgWidth) {
            imgWidth = testWidth;
            imgBoxExtra = getWrapperSpacing(imageSet[i])
          }
        }
        return imgWidth + imgBoxExtra;
      }

      // We want the total of margin, border and padding on the element
      function getWrapperSpacing(el) {
        var spacing = ['margin-left', 'border-left', 'padding-left', 'padding-right', 'border-right', 'margin-right'],
            totalPx = 0,
            spacePx = 0,
            spaceRaw = '';
        for (var i = 0; i < spacing.length; i++) {
          spaceRaw = $(el).css(spacing[i]);

          // Themers might add padding, borders or margin defined in ems, but we can't
          // add that to pixel dimensions returned by naturalWidth, so we just throw
          // away anything but pixels. Themers have to deal with that.
          if(spaceRaw && spaceRaw.substr(spaceRaw.length - 2) == 'px') {
            spacePx = parseInt(spaceRaw, 10);
            totalPx += ($.isNumeric(spacePx)) ? spacePx : 0;
          }
        }
        return totalPx;
      }
    }
  }
})(jQuery);
;

/**
 * @file
 * Add support to html 5 color component
 */
;(function ($) {
  Drupal.behaviors.colorPicker = {
    attach: function(context){
      if(typeof jQuery(".spectrum-color-picker").spectrum === 'function') {
        $(".spectrum-color-picker").spectrum({
          showInput: true,
          allowEmpty: false,
          showAlpha: true,
          showInitial: true,
          preferredFormat: "rgb",
          clickoutFiresChange: true,
          showButtons: true
        });       
      }

    }
  }
})(jQuery);;
/**
 * Visualization for json.
 */

(function ($) {
  Drupal.behaviors.Recline = {
    attach: function (context) {
      if (typeof Drupal.settings.recline !== 'undefined' && typeof Drupal.settings.recline.data !== 'undefined') {
        var json = Drupal.settings.recline.data;
        $('#recline-data-json').JSONView(json);
        $('#recline-data-json').JSONView('collapse');
        $('#toggle-btn').on('click', function(){
          $('#recline-data-json').JSONView('toggle');
        });
      }
    }
  }
})(jQuery);;
/**
 * Visualization for arcgis and rest files.
 */

(function ($) {
  Drupal.behaviors.Recline = {
    attach: function (context) {
      if (typeof Drupal.settings.recline !== 'undefined' && typeof Drupal.settings.recline.url !== 'undefined') {
        var map = L.map('rest-map').setView([Drupal.settings.recline.lat, Drupal.settings.recline.lon], 4);
        var baseLayer = L.esri.basemapLayer('Gray').addTo(map);
        var fl = L.esri.dynamicMapLayer({
          url: Drupal.settings.recline.url,
          opacity: 0.5,
          useCors: false
        }).addTo(map);
        var bounds = L.latLngBounds([]);

        fl.metadata(function(error, metadata){
          let layersIds = metadata.layers.map(l => l.id);
          let counter = sl.length;
          layersIds.forEach(id => {
            L.esri.query({
              url: Drupal.settings.recline.url + '/' + id
            }).bounds(function(error, latLngBounds, response){
              counter--;
              bounds.extend(latLngBounds);
              if(!counter) {
                map.fitBounds(bounds);
              }
            });
          })
        });
      }
    }
  }
})(jQuery);;
